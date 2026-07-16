"""数据模型：GitHub repo 原始数据。"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class RepoData(BaseModel):
    """GitHub 仓库原始数据，来源于 API 响应标准化。"""

    owner: str
    name: str
    full_name: str
    description: str = ""
    topics: list[str] = Field(default_factory=list)
    language: str | None = None
    html_url: str
    starred_at: datetime
    list_name: str = "_uncategorized"

    # 以下字段非 star list API 直接返回，需额外采集
    readme_snippet: str = Field(default="", max_length=2000)
    archived: bool = False
    fork: bool = False
    stargazers_count: int = 0

    @model_validator(mode="after")
    def _check_full_name(self) -> RepoData:
        """确保 full_name 与 owner/name 一致。"""
        expected = f"{self.owner}/{self.name}"
        if self.full_name != expected:
            raise ValueError(
                f"full_name {self.full_name!r} 与 owner/name 组合 {expected!r} 不一致"
            )
        return self
