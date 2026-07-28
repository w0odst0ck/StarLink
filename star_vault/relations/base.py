"""关系引擎 ABC 与注册中心。

所有关系引擎继承 RelationEngine 并实现 analyze_* 方法。
EngineHub 管理引擎注册与获取。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from star_vault.models.repo import RepoData
    from star_vault.models.relation import Relation, GlobalGraph


class RelationEngine(ABC):
    """所有关系引擎的基类。"""

    @property
    @abstractmethod
    def name(self) -> str:
        """引擎唯一标识名，e.g. 'builtin', 'ai'。"""

    @abstractmethod
    def analyze_repo(
        self,
        repo: RepoData,
        all_repos: list[RepoData],
    ) -> list[Relation]:
        """分析单个 repo 与其他 repo 的关系，只返回 source==repo 的。"""

    @abstractmethod
    def analyze_group(
        self,
        repos: list[RepoData],
    ) -> list[Relation]:
        """分析一组 repo 的内部关系（通常同 List），返回不重复的双向关系。"""

    def analyze_global(self, all_repos: list[RepoData]) -> GlobalGraph:
        """全局分析。默认实现：逐 repo 分析 + 去重合并。"""
        edges: list[Relation] = []
        for repo in all_repos:
            edges.extend(self.analyze_repo(repo, all_repos))

        # 去重
        seen: set[tuple[str, str, str]] = set()
        unique: list[Relation] = []
        for e in edges:
            key = (e.source, e.target, str(e.relation_type))
            if key not in seen:
                seen.add(key)
                unique.append(e)

        from star_vault.models.relation import GlobalGraph as _GlobalGraph

        return _GlobalGraph(
            generated_at=datetime.now(),
            engine=self.name,
            nodes=[r.full_name for r in all_repos],
            edges=unique,
        )


class EngineHub:
    """引擎注册中心。"""

    _engines: dict[str, RelationEngine] = {}

    @classmethod
    def register(cls, name: str, engine: RelationEngine) -> None:
        """注册引擎实例。"""
        if not isinstance(engine, RelationEngine):
            raise TypeError(f"{name} 不是 RelationEngine 实例")
        cls._engines[name] = engine

    @classmethod
    def get(cls, name: str) -> RelationEngine:
        """按名称获取引擎实例。"""
        if name not in cls._engines:
            raise KeyError(f"未注册的关系引擎: {name}，可用: {cls.list_engines()}")
        return cls._engines[name]

    @classmethod
    def list_engines(cls) -> list[str]:
        """列出所有已注册引擎。"""
        return list(cls._engines)

    @classmethod
    def load_builtin(cls, config=None) -> None:
        """加载内置引擎。config 给引擎构造用。"""
        from star_vault.relations.engine_builtin import BuiltinEngine

        cls.register("builtin", BuiltinEngine(config))

    @classmethod
    def clear(cls) -> None:
        """清空所有引擎（主要用于测试）。"""
        cls._engines.clear()
