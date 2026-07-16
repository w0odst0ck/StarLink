"""Vault 写入与 slug 生成。"""

from __future__ import annotations

from pathlib import Path

from star_vault.core.template import render_note
from star_vault.models.note import NoteData, TodoItem
from star_vault.models.relation import RelationRef
from star_vault.models.repo import RepoData


def slug_for_repo(owner: str, name: str) -> str:
    """生成文件 slug: 'owner/name' → 'owner.name'（小写）。"""
    return f"{owner}.{name}".lower()


def slug_from_full_name(full_name: str) -> str:
    """'owner/name' → 'owner.name'（小写）。"""
    return full_name.replace("/", ".").lower()


def build_note(
    repo: RepoData,
    *,
    relations: list[RelationRef] | None = None,
    ai_summary: str = "",
    ai_generated: bool = False,
    todo_items: list[TodoItem] | None = None,
) -> NoteData:
    """RepoData → NoteData（自动生成 slug）。"""
    return NoteData(
        slug=slug_from_full_name(repo.full_name),
        title=repo.name,
        repo_full_name=repo.full_name,
        list_name=repo.list_name,
        language=repo.language,
        topics=repo.topics,
        relations=relations or [],
        ai_summary=ai_summary,
        ai_generated=ai_generated,
        todo_items=todo_items or [],
    )


def write_note(note_data: NoteData, vault_path: Path) -> Path:
    """渲染并写入单篇笔记到 vault。

    1. 自动反填 slug（如果为空）
    2. 创建 <vault>/stars/<list_name>/ 目录
    3. 写入 <slug>.md

    返回写入的文件路径。
    """
    vault_path = vault_path.resolve()
    list_dir = vault_path / "stars" / note_data.list_name
    list_dir.mkdir(parents=True, exist_ok=True)

    note_path = list_dir / f"{note_data.slug}.md"
    content = render_note(note_data)
    note_path.write_text(content, encoding="utf-8")

    return note_path
