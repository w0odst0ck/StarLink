"""数据模型：关系类型、关系、聚类与全局关系图。"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum, auto

from pydantic import BaseModel, Field


# ── 关系类型 ──────────────────────────────────────────────


class RelationType(StrEnum):
    """关系类型枚举。扩展仅允许在末尾添加。"""

    SAME_LIST = auto()  # 同 GitHub List
    SIMILAR_TOPICS = auto()  # topics 重叠 ≥ 2
    SAME_LANGUAGE = auto()  # 同语言
    ALTERNATIVE = auto()  # 同领域替代方案
    COMPANION = auto()  # 互补工具
    AI_DISCOVERED = auto()  # AI 隐性关联


# ── 关系数据 ──────────────────────────────────────────────


class RelationRef(BaseModel):
    """笔记中嵌入的轻量关系引用。"""

    target_slug: str
    relation_type: RelationType
    confidence: float = Field(ge=0.0, le=1.0)


class Relation(BaseModel):
    """两个 repo 之间的完整关系。"""

    source: str  # 源 repo full_name
    target: str  # 目标 repo full_name
    relation_type: RelationType
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    metadata: dict = Field(default_factory=dict)
    # 规则匹配时的匹配细节
    # e.g. {"matched_topics": ["llm", "embedding"]}


# ── 聚类 ──────────────────────────────────────────────────


class Cluster(BaseModel):
    """关系聚类。"""

    id: str
    name: str
    repos: list[str]  # repo full_name 列表
    dominant_topics: list[str] = Field(default_factory=list)
    ai_label: str | None = None


# ── 全局关系图 ──────────────────────────────────────────────


class GlobalGraph(BaseModel):
    """全局关系图。

    注意：orphans（无关联 repo）是衍生值，不存入文件。
    使用 compute_orphans() 实时计算。
    """

    generated_at: datetime
    engine: str
    nodes: list[str]  # 所有涉及关系 repo 的 full_name
    edges: list[Relation]
    clusters: list[Cluster] = Field(default_factory=list)

    def relations_for(self, repo: str, min_confidence: float = 0.0) -> list[Relation]:
        """获取指定 repo 的关系（作为 source 或 target）。"""
        return [
            e
            for e in self.edges
            if (e.source == repo or e.target == repo)
            and e.confidence >= min_confidence
        ]

    def compute_orphans(self, all_repos: set[str]) -> list[str]:
        """实时计算无关联 repo。"""
        related: set[str] = set()
        for e in self.edges:
            related.add(e.source)
            related.add(e.target)
        return sorted(all_repos - related)
