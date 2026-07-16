"""GitHub starred repos 同步引擎。

支持全量 sync 和 cutoff 增量 sync（拉到比上次 sync 旧的 repo 即停）。
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import httpx

from star_vault.core.config import Config
from star_vault.core.state import RepoState, StateManager
from star_vault.models.repo import RepoData

logger = logging.getLogger(__name__)

_API_BASE = "https://api.github.com"
_PAGE_SIZE = 100

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
        "User-Agent": "StarLink/0.1",
    }


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

    owner_login = (
        repo["owner"]["login"]
        if isinstance(repo.get("owner"), dict)
        else repo.get("owner", "")
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
        else datetime.min,
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
    page = 1

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

            page += 1

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

    # 拉取
    fetched = fetch_starred(
        config.github.token,
        limit=limit,
        cutoff=cutoff,
    )

    result = SyncResult(total_fetched=len(fetched))

    for repo in fetched:
        # Phase 0 简化：full_name 作为变更标识
        current_sha = repo.full_name

        if sm.needs_sync(repo.full_name, current_sha):
            if sm.get_repo(repo.full_name) is None:
                result.new_repos.append(repo)
            else:
                result.updated_repos.append(repo)

            # 更新状态
            sm.upsert_repo(
                repo.full_name,
                RepoState(
                    starred_at=repo.starred_at,
                    list_name=repo.list_name,
                    sha=current_sha,
                    ai_analyzed=False,
                ),
            )
        else:
            result.unchanged_count += 1
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
