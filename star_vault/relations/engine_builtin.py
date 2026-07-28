"""可组合的规则引擎：Rule ABC、内置规则、BuiltinEngine。

设计原则：
  - 每条规则定义一对 repo 的某种关系发现策略
  - 多条规则对同一对 repo 可并列产出不同类型的关系（无 break）
  - 领域检测仅基于 topics（标签），不做 description 分词
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from star_vault.models.repo import RepoData
from star_vault.models.relation import Relation, RelationType, GlobalGraph
from star_vault.relations.base import RelationEngine


# ── 规则抽象 ──────────────────────────────────────────


class Rule(ABC):
    """单条关系发现规则。"""

    priority: int = 0
    relation_type: RelationType | None = None

    @abstractmethod
    def apply(self, repo: RepoData, candidate: RepoData) -> Relation | None:
        """评估 repo 与 candidate 之间的关系。"""

    @abstractmethod
    def metadata(self) -> dict:
        """返回规则描述信息。"""


# ── 领域关键词表 ──────────────────────────────────────────


DOMAIN_KEYWORDS: dict[str, set[str]] = {
    "web": {"web", "http", "rest", "api", "backend", "frontend", "framework"},
    "ai": {
        "machine-learning", "deep-learning", "llm", "nlp", "neural",
        "transformer", "artificial-intelligence", "embedding", "rag",
    },
    "database": {"database", "sql", "nosql", "orm", "query", "redis", "postgresql"},
    "devops": {"ci", "cd", "deploy", "docker", "kubernetes", "monitoring", "devops"},
    "cli": {"cli", "command-line", "terminal", "shell"},
    "data": {"data", "analytics", "pipeline", "etl", "visualization", "big-data"},
    "mobile": {"mobile", "ios", "android", "flutter", "react-native"},
    "security": {"security", "auth", "authentication", "encryption", "oauth"},
}


# ── 规则实现 ──────────────────────────────────────────


class TopicOverlapRule(Rule):
    """Topics 交集 ≥ 2 产出 SIMILAR_TOPICS 关系。"""

    priority = 20
    relation_type = RelationType.SIMILAR_TOPICS

    def apply(self, repo: RepoData, candidate: RepoData) -> Relation | None:
        overlap = set(repo.topics) & set(candidate.topics)
        if len(overlap) >= 2:
            confidence = min(1.0, len(overlap) * 0.3 + 0.2)
            return Relation(
                source=repo.full_name,
                target=candidate.full_name,
                relation_type=self.relation_type,
                confidence=round(confidence, 2),
                metadata={"matched_topics": sorted(overlap)},
            )
        return None

    def metadata(self) -> dict:
        return {"name": "TopicOverlapRule", "threshold": 2}


class LanguageDomainRule(Rule):
    """同语言 + 同领域产出 ALTERNATIVE 关系。

    领域检测仅基于 topics（标签），避开 description 自然语言噪音。
    """

    priority = 30
    relation_type = RelationType.ALTERNATIVE

    def apply(self, repo: RepoData, candidate: RepoData) -> Relation | None:
        if not repo.language or repo.language != candidate.language:
            return None

        repo_domains = self._detect_domains(repo)
        cand_domains = self._detect_domains(candidate)
        common = repo_domains & cand_domains

        if common:
            confidence = min(0.8, 0.3 + len(common) * 0.2)
            return Relation(
                source=repo.full_name,
                target=candidate.full_name,
                relation_type=self.relation_type,
                confidence=round(confidence, 2),
                metadata={"language": repo.language, "domains": sorted(common)},
            )
        return None

    @staticmethod
    def _detect_domains(repo: RepoData) -> set[str]:
        """基于 topics 检测 repo 所属领域。"""
        topics = set(t.lower() for t in repo.topics)
        return {d for d, kw in DOMAIN_KEYWORDS.items() if topics & kw}

    def metadata(self) -> dict:
        return {"name": "LanguageDomainRule", "domains": list(DOMAIN_KEYWORDS)}


# ── 内置引擎 ──────────────────────────────────────────


class BuiltinEngine(RelationEngine):
    """内置规则引擎：组合规则链 + 编排执行。

    多条规则对同一对 repo 可并列产出不同类型的关系。
    """

    def __init__(self, config=None) -> None:
        self._rules: list[Rule] = [TopicOverlapRule(), LanguageDomainRule()]

    @property
    def name(self) -> str:
        return "builtin"

    def analyze_repo(
        self,
        repo: RepoData,
        all_repos: list[RepoData],
    ) -> list[Relation]:
        relations: list[Relation] = []
        for candidate in all_repos:
            if candidate.full_name == repo.full_name:
                continue
            for rule in sorted(self._rules, key=lambda r: r.priority):
                rel = rule.apply(repo, candidate)
                if rel:
                    relations.append(rel)
                    # 不 break — 允许多条规则对同一对 repo 产出不同关系
        return relations

    def analyze_group(self, repos: list[RepoData]) -> list[Relation]:
        """组内所有 repo 两两分析。"""
        relations: list[Relation] = []
        for i, repo in enumerate(repos):
            for candidate in repos[i + 1 :]:
                relations.extend(self.analyze_repo(repo, [candidate]))
        return relations
