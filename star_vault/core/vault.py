"""Vault 写入与 slug 生成。"""

from __future__ import annotations

from pathlib import Path

from star_vault.core.template import render_note
from star_vault.models.note import NoteData


def slug_for_repo(owner: str, name: str) -> str:
    """生成文件 slug: 'owner/name' → 'owner.name'（小写）。

    注意：slug 不可逆（a.b/c → a.b.c 与 a/b.c → a.b.c 冲突）。
    实际概率极低，Phase 0 不做去重。
    """
    return f"{owner}.{name}".lower()


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
