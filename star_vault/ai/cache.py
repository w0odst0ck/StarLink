"""AI 缓存：基于输入 hash 的文件缓存。

缓存键 = sha256(model + owner/name + topics + readme_snippet 前500字)。
不同模型使用不同缓存键，互不干扰。
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from star_vault.models.repo import RepoData


class AICache:
    """AI 分析结果的文件缓存。

    缓存路径：<vault>/.ai-cache/<hash>.json
    """

    def __init__(self, cache_dir: Path, model: str = "") -> None:
        self._dir = cache_dir / ".ai-cache"
        self._dir.mkdir(parents=True, exist_ok=True)
        self._model = model

    def get(self, repo: RepoData) -> dict | None:
        """读取缓存，命中返回 dict，未命中返回 None。"""
        path = self._path(repo)
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    def set(self, repo: RepoData, data: dict) -> None:
        """写入缓存。"""
        path = self._path(repo)
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _path(self, repo: RepoData) -> Path:
        return self._dir / f"{self._key(repo)}.json"

    def _key(self, repo: RepoData) -> str:
        """缓存键：model + owner/name + topics + readme_snippet 前500。

        使用 sha256 前 16 字符作为文件名，避免文件名过长。
        """
        raw = (
            f"{self._model}:{repo.owner}/{repo.name}:"
            f"{sorted(repo.topics)}:{repo.readme_snippet[:500]}"
        )
        return hashlib.sha256(raw.encode()).hexdigest()[:16]
