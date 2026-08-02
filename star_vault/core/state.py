"""同步状态管理。

记录每个 repo 的同步状态（starred_at / sha / AI 状态），
支持增量同步的判断：needs_sync() / needs_ai()。
"""

from __future__ import annotations

import fcntl
import json
import os
from datetime import datetime
from pathlib import Path

import pydantic
from pydantic import BaseModel, Field

from star_vault.core.config import json_dumps


# AI 状态枚举
AI_STATUS_PENDING = "pending"
AI_STATUS_DONE = "done"
AI_STATUS_FAILED = "failed"
AI_STATUS_STALE = "stale"
AI_STATUS_LOCKED = "locked"


# ── 状态数据模型 ──────────────────────────────────────────
# 注：此处定义是 0.1 内嵌设计，0.2 数据模型阶段可能重构至 models/


class RepoState(BaseModel):
    """单个 repo 的同步记录。"""

    starred_at: datetime
    list_name: str = "_uncategorized"
    sha: str = ""
    ai_analyzed: bool = False  # 旧字段，继承兼容
    ai_cache_key: str = ""
    readme_fetched: bool = False
    ai_status: str = AI_STATUS_PENDING

    # Repo 元数据（用于 --ai-only 重建）
    language: str = ""
    topics: list[str] = Field(default_factory=list)
    description: str = ""


class StateFile(BaseModel):
    """状态文件顶层结构。"""

    version: int = 1
    last_sync_at: datetime | None = None
    repos: dict[str, RepoState] = Field(default_factory=dict)
    # key = repo full_name (owner/repo)


# ── 状态管理器 ──────────────────────────────────────────────


class StateManager:
    """状态文件读写与查询。

    用法：
        sm = StateManager(Path("./vault"))
        sf = sm.load()
        sm.upsert_repo("owner/repo", RepoState(...))
        sm.save()
    """

    def __init__(self, vault_path: Path, state_relpath: str = ".star-vault-state.json") -> None:
        """初始化状态管理器。

        参数：
            vault_path: vault 根目录（自动 resolve 为绝对路径）
            state_relpath: 状态文件相对 vault 根路径
        """
        self._state_path = vault_path.resolve() / state_relpath
        self._current: StateFile = StateFile()

    # ── 公共接口 ────────────────────────────────────────────

    @property
    def state_path(self) -> Path:
        """状态文件的绝对路径。"""
        return self._state_path

    def load(self) -> StateFile:
        """加载状态文件，不存在则返回空 StateFile。"""
        if not self._state_path.is_file():
            self._current = StateFile()
            return self._current
        try:
            raw = self._state_path.read_text(encoding="utf-8")
            self._current = StateFile.model_validate_json(raw)
        except (json.JSONDecodeError, pydantic.ValidationError, OSError) as exc:
            raise RuntimeError(
                f"状态文件损坏或无法读取: {self._state_path}: {exc}"
            ) from exc
        return self._current

    def save(self) -> None:
        """原子写入状态文件。

        写临时文件到同目录 → os.replace() 替换。
        同目录 replace 不跨文件系统，保证原子性。
        """
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        data = self._current.model_dump(mode="json")
        content = json_dumps(data)
        _atomic_write(self._state_path, content)

    def get_repo(self, full_name: str) -> RepoState | None:
        """获取指定 repo 的状态，不存在返回 None。"""
        return self._current.repos.get(full_name)

    def upsert_repo(self, full_name: str, state: RepoState) -> None:
        """更新或插入 repo 状态。"""
        self._current.repos[full_name] = state

    def needs_sync(self, repo_full_name: str, current_sha: str) -> bool:
        """判断 repo 是否需要同步处理。

        规则：
          - 新 repo → True
          - sha 变化 → True（内容变更）
          - 已同步且 sha 相同 → False
        """
        existing = self._current.repos.get(repo_full_name)
        if existing is None:
            return True
        return existing.sha != current_sha

    def needs_ai(self, repo_full_name: str) -> bool:
        """判断 repo 是否需要 AI 分析。

        规则（ai_status 三级状态优先，ai_analyzed 旧字段兜底）：
          - done/locked → False（已分析 / 人工锁定，不重跑）
          - failed/stale → True（失败 / 过期，重跑）
          - 其余（空状态）→ 回退旧字段 ai_analyzed
        """
        existing = self._current.repos.get(repo_full_name)
        if existing is None:
            return True
        if existing.ai_status in (AI_STATUS_DONE, AI_STATUS_LOCKED):
            return False
        if existing.ai_status in (AI_STATUS_FAILED, AI_STATUS_STALE):
            return True
        return not existing.ai_analyzed

    def needs_reanalysis(
        self, repo_full_name: str, current_key: str = ""
    ) -> bool:
        """判断是否需要重新 AI 分析（三级状态兼容旧数据）。"""
        existing = self._current.repos.get(repo_full_name)
        if existing is None:
            return True
        # 空字符串 ai_status 不视为有效值，回退到旧字段
        status = existing.ai_status
        if not status:
            status = AI_STATUS_DONE if existing.ai_analyzed else AI_STATUS_PENDING
        if status == AI_STATUS_LOCKED:
            return False
        if status in (AI_STATUS_PENDING, AI_STATUS_FAILED, AI_STATUS_STALE):
            return True
        if status == AI_STATUS_DONE and current_key and existing.ai_cache_key != current_key:
            return True
        return False

    def get_new_repos_since(self, since: datetime) -> list[str]:
        """获取指定时间后 star 的 repo 列表。"""
        return [
            full_name
            for full_name, rs in self._current.repos.items()
            if rs.starred_at > since
        ]


# ── 工具函数 ──────────────────────────────────────────────


def _atomic_write(path: Path, content: str) -> None:
    """同目录原子写入（带文件锁）。

    写 .tmp 临时文件 → os.replace() 替换原文件。
    同目录 replace 为 POSIX 原子操作。
    文件锁防止多进程并发写入产生竞态。
    """
    tmp = path.with_suffix(".tmp")
    tmp.write_text(content, encoding="utf-8")
    with open(path, "a") as lock_f:
        fcntl.flock(lock_f.fileno(), fcntl.LOCK_EX)
        os.replace(tmp, path)
        fcntl.flock(lock_f.fileno(), fcntl.LOCK_UN)
