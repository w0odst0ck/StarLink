"""Vault 写入与 slug 生成。"""

from __future__ import annotations

import logging
from pathlib import Path

from star_vault.core.template import render_note
from star_vault.models.note import NoteData, TodoItem
from star_vault.models.relation import RelationRef
from star_vault.models.repo import RepoData

logger = logging.getLogger(__name__)

_HUMAN_EDITED_MARK = "human_edited: true"


def slug_for_repo(owner: str, name: str) -> str:
    """生成文件 slug: 'owner/name' → 'owner.name'（小写）。"""
    return f"{owner}.{name}".lower()


def slug_from_full_name(full_name: str) -> str:
    """'owner/name' → 'owner.name'（小写）。"""
    return full_name.replace("/", ".").lower()


def _find_slug_files(vault_path: Path, slug: str) -> list[Path]:
    """全库查找同 slug 笔记文件（含其他分类目录）。"""
    stars_root = vault_path / "stars"
    if not stars_root.is_dir():
        return []
    return [p for p in stars_root.rglob("*.md") if p.stem == slug]


def build_note(
    repo: RepoData,
    *,
    relations: list[RelationRef] | None = None,
    ai_summary: str = "",
    ai_generated: bool = False,
    todo_items: list[TodoItem] | None = None,
    category: str = "",
    rating: int = 0,
    maintenance: str = "",
    ai_tags: list[str] | None = None,
) -> NoteData:
    """RepoData → NoteData（自动生成 slug）。"""
    return NoteData(
        slug=slug_from_full_name(repo.full_name),
        title=repo.name,
        repo_full_name=repo.full_name,
        list_name=repo.list_name,
        description=repo.description,
        language=repo.language,
        topics=repo.topics,
        relations=relations or [],
        ai_summary=ai_summary,
        ai_generated=ai_generated,
        todo_items=todo_items or [],
        category=category,
        rating=rating,
        maintenance=maintenance,
        ai_tags=ai_tags or [],
    )


def write_note(
    note_data: NoteData,
    vault_path: Path,
    *,
    force: bool = False,
) -> Path:
    """渲染并写入单篇笔记到 vault。

    1. 自动反填 slug（如果为空）
    2. 创建 <vault>/stars/<list_name>/ 目录
    3. 写入 <slug>.md

    human_edited 保护：目标文件已含 `human_edited: true` 时默认跳过写入
    （人工编辑优先，除非 force=True 显式覆盖）。

    返回写入的文件路径。

    异常：
        ValueError: 无法确定 slug
        RuntimeError: 文件写入失败或为空
    """
    vault_path = vault_path.resolve()

    # 自动反填 slug
    slug = note_data.slug or slug_from_full_name(note_data.repo_full_name)
    if not slug:
        raise ValueError(
            f"无法确定 slug: repo_full_name={note_data.repo_full_name!r}"
        )

    list_dir = vault_path / "stars" / note_data.list_name
    list_dir.mkdir(parents=True, exist_ok=True)

    note_path = list_dir / f"{slug}.md"

    # slug 唯一性拦截（锚点语义）：全库同 slug 只允许一份
    # 背景：sync 按 GitHub 实时 list 落盘，人工分类与 GitHub list 不一致时
    #       会在另一目录重复写一份模板版 → 历史 17 个重复副本即由此产生。
    # 规则：
    #   - 别处存在 human_edited 人工版 → 人工版是锚点，跳过写入（保留人工分类）
    #   - 别处存在模板版（孤儿副本）→ 删除，保证任意时刻每 slug 仅一份
    for other in _find_slug_files(vault_path, slug):
        if other == note_path:
            continue
        if _HUMAN_EDITED_MARK in other.read_text(encoding="utf-8"):
            logger.warning(
                "跳过写入：slug %s 的人工版在 %s（list 归属不一致，保留人工版）",
                slug,
                other,
            )
            return other
        other.unlink()
        logger.info("清理孤儿副本 %s（slug 唯一化）", other)

    # human_edited 保护：人工编辑过的笔记不覆盖（除非 force）
    if not force and note_path.is_file():
        existing = note_path.read_text(encoding="utf-8")
        if _HUMAN_EDITED_MARK in existing:
            logger.info("跳过人工编辑笔记（human_edited 保护）: %s", note_path)
            return note_path

    content = render_note(note_data)
    note_path.write_text(content, encoding="utf-8")

    # 写入后校验
    if not note_path.exists() or note_path.stat().st_size == 0:
        raise RuntimeError(f"笔记写入失败或内容为空: {note_path}")

    return note_path
