"""数据模型：Vault 笔记与 TODO 项。"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from star_vault.models.relation import RelationRef


class TodoItem(BaseModel):
    """单个 TODO 项。"""

    text: str
    source_repo: str  # owner/name
    priority: int = Field(default=3, ge=1, le=5)
    done: bool = False


class NoteData(BaseModel):
    """Vault 中单篇 repo 笔记的完整表示。"""

    slug: str  # 文件名（不含扩展），e.g. "pallets.flask"
    title: str  # 显示用标题，通常 = name
    repo_full_name: str
    list_name: str

    # Frontmatter
    language: str | None = None
    topics: list[str] = Field(default_factory=list)
    status: Literal["unreviewed", "reviewed", "archived"] = "unreviewed"
    ai_generated: bool = False

    # 内容
    ai_summary: str = ""
    todo_items: list[TodoItem] = Field(default_factory=list)
    relations: list[RelationRef] = Field(default_factory=list)
