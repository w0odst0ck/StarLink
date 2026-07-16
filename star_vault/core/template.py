"""笔记模板渲染器。

将 NoteData 渲染为 Markdown vault 笔记。
模板目录默认自动定位到 star_vault/templates/。
"""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from star_vault.models.note import NoteData
from star_vault.models.relation import RelationType

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"


def _confidence_label(confidence: float) -> str:
    """置信度转中文标签。"""
    if confidence >= 0.8:
        return "高"
    if confidence >= 0.5:
        return "中"
    return "低"


def _format_relation_notes(note_data: NoteData) -> list[dict]:
    """展开 RelationRef 为模板需要的 dict 列表。"""
    return [
        {
            "name": ref.target_slug,
            "type": ref.relation_type.name.replace("_", " ").title(),
            "confidence": _confidence_label(ref.confidence),
        }
        for ref in note_data.relations
    ]


def render_note(
    note_data: NoteData,
    *,
    template_dir: Path | None = None,
) -> str:
    """将 NoteData 渲染为 Markdown 笔记。

    参数：
        note_data: 笔记数据（来自 NoteData 模型）
        template_dir: 模板目录，默认自动定位到 star_vault/templates/
    """
    env = Environment(
        loader=FileSystemLoader(str(template_dir or _TEMPLATE_DIR)),
        autoescape=False,
    )
    tmpl = env.get_template("repo.md.j2")

    # 模板期望的上下文：repo 对象 + 列表字段
    class _RepoProxy:
        """模板内用 repo.name / repo.full_name 等访问。"""
        def __init__(self, note: NoteData) -> None:
            self.full_name = note.repo_full_name
            self.name = note.title
            self.description = ""
            self.language = note.language or ""
            self.topics = note.topics

    context = {
        "repo": _RepoProxy(note_data),
        "relations": [ref.target_slug for ref in note_data.relations],
        "ai_generated": note_data.ai_generated,
        "ai_summary": note_data.ai_summary,
        "todo_items": note_data.todo_items,
        "relation_notes": _format_relation_notes(note_data),
    }

    return tmpl.render(**context)
