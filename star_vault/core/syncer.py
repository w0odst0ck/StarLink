"""GitHub starred repos 同步引擎。

支持全量 sync 和 cutoff 增量 sync（拉到比上次 sync 旧的 repo 即停）。
"""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import httpx

from star_vault.core.config import Config
from star_vault.core.state import RepoState, StateManager, AI_STATUS_PENDING
from star_vault.models.repo import RepoData

logger = logging.getLogger(__name__)

_API_BASE = "https://api.github.com"
_PAGE_SIZE = 100
_USER_AGENT = "StarLink/0.1"

# ── 异常 ──────────────────────────────────────────────


class SyncError(Exception):
    """同步过程中可恢复的错误。"""


# ── 结果类型 ──────────────────────────────────────────────


@dataclass
class SyncResult:
    """单次 sync 的结果汇总。"""

    new_repos: list[RepoData] = field(default_factory=list)
    updated_repos: list[RepoData] = field(default_factory=list)
    ai_pending: list[RepoData] = field(default_factory=list)
    unchanged_count: int = 0
    total_fetched: int = 0


# ── 内部类型 ──────────────────────────────────────────────


def _build_headers(token: str) -> dict[str, str]:
    """构建 GitHub API 请求头，含 star+json 媒体类型。"""
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3.star+json",
        "User-Agent": _USER_AGENT,
    }


def _build_graphql_headers(token: str) -> dict[str, str]:
    """构建 GitHub GraphQL API 请求头。"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": _USER_AGENT,
    }


_QUERY_LISTS = """
query {
    viewer {
        lists(first: 50) {
            nodes { id name }
        }
    }
}
"""

_QUERY_LIST_ITEMS = """
query($id: ID!, $after: String) {
    node(id: $id) {
        ... on UserList {
            items(first: 100, after: $after) {
                pageInfo { hasNextPage endCursor }
                nodes { ... on Repository { nameWithOwner } }
            }
        }
    }
}
"""


def fetch_user_lists(token: str) -> dict[str, str]:
    """
    通过 GraphQL 查询用户的 Star Lists，返回 {full_name: list_name} 映射。

    对应 GitHub Web UI 上的 starred repo 分类。
    """
    headers = _build_graphql_headers(token)
    list_repos: dict[str, str] = {}

    with httpx.Client(timeout=30) as client:
        # 1. 获取所有 lists
        resp = client.post(
            f"{_API_BASE}/graphql",
            headers=headers,
            json={"query": _QUERY_LISTS},
        )
        resp.raise_for_status()
        data = resp.json()
        lists = data.get("data", {}).get("viewer", {}).get("lists", {}).get("nodes", [])

        if not lists:
            logger.info("未找到 GitHub Star Lists")
            return list_repos

        # 2. 逐 list 获取 repo 列表
        for lst in lists:
            lid = lst["id"]
            lname = lst["name"]
            cursor: str | None = None
            list_count = 0

            while True:
                variables: dict[str, object] = {"id": lid, "after": cursor}
                item_resp = client.post(
                    f"{_API_BASE}/graphql",
                    headers=headers,
                    json={"query": _QUERY_LIST_ITEMS, "variables": variables},
                )
                item_resp.raise_for_status()
                item_data = item_resp.json()
                items_node = item_data.get("data", {}).get("node", {}).get("items", {})
                nodes = items_node.get("nodes", [])

                for n in nodes:
                    if n and n.get("nameWithOwner"):
                        list_repos[n["nameWithOwner"]] = lname
                        list_count += 1

                # 分页
                page_info = items_node.get("pageInfo", {})
                if page_info.get("hasNextPage") and page_info.get("endCursor"):
                    cursor = page_info["endCursor"]
                else:
                    break

            logger.info("  List %s: %d repo(s)", lname, list_count)

    logger.info("共 %d 个 List, %d 个 repo 有分类", len(lists), len(list_repos))
    return list_repos


def _parse_starred_item(item: dict[str, Any]) -> RepoData:
    """将 GitHub API 返回的 star 条目解析为 RepoData。

    支持两种格式：
      star+json:  {"starred_at": ..., "repo": {full_name, ...}}
      默认 v3:    {full_name, ...}（无 starred_at）
    """
    if "repo" in item:
        # star+json 格式
        repo = item["repo"]
        starred_at_str = item.get("starred_at", "")
    else:
        # 默认 v3 格式
        repo = item
        starred_at_str = ""

    owner_dict = repo.get("owner", {})
    owner_login = (
        owner_dict.get("login", "")
        if isinstance(owner_dict, dict)
        else str(owner_dict)
    )
    owner_name = repo["full_name"].split("/")[0]

    return RepoData(
        owner=owner_login or owner_name,
        name=repo["name"],
        full_name=repo["full_name"],
        description=repo.get("description") or "",
        topics=repo.get("topics") or [],
        language=repo.get("language"),
        html_url=repo.get("html_url", ""),
        starred_at=datetime.fromisoformat(starred_at_str.replace("Z", "+00:00"))
        if starred_at_str
        else datetime.min.replace(tzinfo=timezone.utc),
        list_name="_uncategorized",
        archived=repo.get("archived", False),
        fork=repo.get("fork", False),
        stargazers_count=repo.get("stargazers_count", 0),
    )


def _fetch_page(
    client: httpx.Client,
    url: str,
    headers: dict[str, str],
    params: dict[str, Any],
) -> tuple[list[dict[str, Any]], str | None]:
    """拉取单页数据，返回 (items, next_url)。"""
    resp = client.get(url, headers=headers, params=params)

    # 处理 GitHub API 错误
    if resp.status_code == 401:
        raise SyncError("GitHub token 无效或已过期，请检查 GH_TOKEN")
    if resp.status_code == 403:
        reset_ts = resp.headers.get("X-RateLimit-Reset", "")
        msg = f"GitHub API 限流 (403)。"
        if reset_ts:
            from datetime import datetime as _dt
            reset_time = _dt.fromtimestamp(int(reset_ts))
            msg += f" 重置时间: {reset_time.isoformat()}"
        raise SyncError(msg)
    resp.raise_for_status()

    items = resp.json()
    if not isinstance(items, list):
        raise SyncError(f"非预期的 API 响应格式: {type(items)}")

    # 解析 Link header 获取下一页
    next_url: str | None = None
    link = resp.headers.get("link", "")
    for part in link.split(","):
        if 'rel="next"' in part:
            start = part.index("<") + 1
            end = part.index(">")
            next_url = part[start:end]
            break

    return items, next_url


def fetch_starred(
    token: str,
    *,
    limit: int | None = None,
    cutoff: datetime | None = None,
) -> list[RepoData]:
    """从 GitHub API 拉取 starred repos。

    参数：
        token: GitHub PAT
        limit: 最多拉取数（None=无限制）
        cutoff: 增量 cutoff，遇到 starred_at <= cutoff 即停

    返回：RepoData 列表（按 star 时间降序）
    """
    headers = _build_headers(token)
    repos: list[RepoData] = []

    next_url: str | None = None
    per_page = min(100, limit or 100)

    with httpx.Client(timeout=30) as client:
        while True:
            if next_url:
                url = next_url
                params: dict[str, Any] = {}
            else:
                url = f"{_API_BASE}/user/starred"
                params = {"per_page": max(1, per_page)}

            items, next_url = _fetch_page(client, url, headers, params)

            for item in items:
                repo = _parse_starred_item(item)

                # cutoff 检查：当前 repo 比 cutoff 还旧 → 停
                if cutoff and repo.starred_at <= cutoff:
                    logger.info(
                        "cutoff 触发: %s at %s", repo.full_name, repo.starred_at
                    )
                    return repos

                repos.append(repo)

                # limit 检查
                if limit and len(repos) >= limit:
                    logger.info("limit 触发: %d repos", len(repos))
                    return repos[:limit]

            if not next_url:
                break


    return repos


def sync(
    config: Config,
    mode: str = "full",
    limit: int | None = None,
) -> SyncResult:
    """执行一次同步。

    参数：
        config: 配置对象（需含 github.token）
        mode: "full" | "incremental"
        limit: 限制拉取数（主要用于测试）

    返回：SyncResult
    """
    from pathlib import Path

    vault_path = Path(config.vault.path).expanduser().resolve()
    sm = StateManager(vault_path, state_relpath=config.state.path)
    state = sm.load()

    # 确定 cutoff
    cutoff: datetime | None = None
    if mode == "incremental" and state.last_sync_at:
        cutoff = state.last_sync_at
        logger.info("增量模式: cutoff = %s", cutoff)

    # 拉取 GitHub Star Lists 分类
    list_map = fetch_user_lists(config.github.token)

    # 拉取
    fetched = fetch_starred(
        config.github.token,
        limit=limit,
        cutoff=cutoff,
    )

    result = SyncResult(total_fetched=len(fetched))

    for repo in fetched:
        # 根据 GitHub Star List 覆盖 list_name
        repo.list_name = list_map.get(repo.full_name, repo.list_name)
        # 取可变字段哈希作为变更标识（description/topics/language/stargazers 变化时触发 resync）
        _content_key = f"{repo.description}|{sorted(repo.topics)}|{repo.language}|{repo.stargazers_count}"
        current_sha = hashlib.sha256(_content_key.encode()).hexdigest()[:16]

        if sm.needs_sync(repo.full_name, current_sha):
            if sm.get_repo(repo.full_name) is None:
                result.new_repos.append(repo)
            else:
                result.updated_repos.append(repo)

            # 更新状态（保留已有 AI 状态，仅内容变更时不重置 AI）
            existing_state = sm.get_repo(repo.full_name)
            if existing_state:
                ai_analyzed = existing_state.ai_analyzed
                ai_status = existing_state.ai_status
            else:
                ai_analyzed = False
                ai_status = AI_STATUS_PENDING

            sm.upsert_repo(
                repo.full_name,
                RepoState(
                    starred_at=repo.starred_at,
                    list_name=repo.list_name,
                    sha=current_sha,
                    ai_analyzed=ai_analyzed,
                    ai_status=ai_status,
                    language=repo.language or "",
                    topics=repo.topics,
                    description=repo.description or "",
                ),
            )
        else:
            result.unchanged_count += 1
            # 即使内容未变，也更新 list_name（GitHub List 分类可能手动调整过）
            existing = sm.get_repo(repo.full_name)
            if existing and existing.list_name != repo.list_name:
                existing.list_name = repo.list_name
                sm.upsert_repo(repo.full_name, existing)
            if sm.needs_ai(repo.full_name):
                result.ai_pending.append(repo)

    # 更新 sync 时间
    state.last_sync_at = datetime.now(timezone.utc)
    sm.save()

    logger.info(
        "sync 完成: 新增=%d, 更新=%d, 未变=%d",
        len(result.new_repos),
        len(result.updated_repos),
        result.unchanged_count,
    )

    return result
