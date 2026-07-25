"""GitHub Pages 站点数据生成。

scan_vault_notes() 扫描 vault/stars/ 目录，解析全部笔记 markdown 文件，
产出 site-data.json 供前端 SPA 使用。

用法：
    star-vault sync --with-pages    # 同步后生成页面
    star-vault pages                # 从已有 vault 重新生成
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

_PAGES_STATIC = ("index.html", "app.js", "style.css")

# ── 扫描 vault ──────────────────────────────────────


def scan_vault_notes(vault_path: Path) -> list[dict]:
    """扫描 vault/stars/ 下所有 .md 笔记，返回结构化数据列表。"""
    stars_dir = vault_path / "stars"
    if not stars_dir.is_dir():
        return []

    notes: list[dict] = []
    for md_file in sorted(stars_dir.rglob("*.md")):
        note = _parse_note_file(md_file)
        if note:
            notes.append(note)

    return notes


def _parse_note_file(path: Path) -> dict | None:
    """解析单篇笔记 markdown 文件。"""
    content = path.read_text(encoding="utf-8")

    # 解析 frontmatter（--- 块）
    fm = _parse_frontmatter(content)
    if not fm:
        return None

    # 提取 body 中的结构化内容
    body = _parse_body(content)

    return {
        "slug": path.stem,
        "title": body.get("title", path.stem),
        "repo_full_name": fm.get("repo", ""),
        "list_name": path.parent.name,
        "language": (fm.get("language") or "") or None,
        "topics": fm.get("topics", []),
        "status": fm.get("status", "unreviewed"),
        "ai_generated": fm.get("ai_generated", False),
        "ai_summary": body.get("ai_summary", ""),
        "todo_items": body.get("todo_items", []),
        "relations": _parse_relations(fm.get("relations", [])),
    }


def _parse_frontmatter(content: str) -> dict:
    """解析 --- 分隔的 frontmatter。"""
    m = re.match(r"^---\n(.+?)\n---", content, re.DOTALL)
    if not m:
        return {}

    result: dict = {}
    for line in m.group(1).split("\n"):
        line = line.strip()
        if not line or ":" not in line:
            continue

        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"')

        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            result[key] = [x.strip() for x in inner.split(",")] if inner else []
        elif value.lower() in ("true", "false"):
            result[key] = value.lower() == "true"
        else:
            result[key] = value

    return result


def _parse_body(content: str) -> dict:
    """从 markdown body 提取标题、AI 摘要、TODO 项。"""
    result: dict = {"title": "", "ai_summary": "", "todo_items": []}

    # 去掉 frontmatter
    body = re.sub(r"^---\n.*?\n---\n", "", content, count=1, flags=re.DOTALL)
    body = body.lstrip()  # 去掉前导空行

    # 标题：# repo-name
    title_m = re.match(r"# (.+)", body)
    if title_m:
        result["title"] = title_m.group(1).strip()

    # AI 摘要：## ✦ AI 摘要 后直到下一个 ## 或结尾
    summary_m = re.search(r"## ✦ AI 摘要\n\n(.+?)(?=\n## |\Z)", body, re.DOTALL)
    if summary_m:
        result["ai_summary"] = summary_m.group(1).strip()

    # TODO 项：## TODO 下的 - [ ] / - [x] 列表
    todo_m = re.search(r"## TODO\n\n(.+?)(?=\n## |\Z)", body, re.DOTALL)
    if todo_m:
        items: list[dict] = []
        for line in todo_m.group(1).split("\n"):
            line = line.strip()
            tm = re.match(r"- \[([ x])\] (.+)", line)
            if tm:
                done = tm.group(1) == "x"
                text = tm.group(2).strip()
                priority = 3
                pm = re.search(r"\(P([1-5])\)", text)
                if pm:
                    priority = int(pm.group(1))
                    text = text.rsplit("(", 1)[0].strip()
                items.append({"text": text, "done": done, "priority": priority})
        result["todo_items"] = items

    return result


def _parse_relations(rels: list) -> list[dict]:
    """解析 frontmatter relations: target_slug: TYPE(confidence)"""
    result: list[dict] = []
    for rel in rels:
        m = re.match(r"(.+?): (\w+)\(([\d.]+)\)", rel)
        if m:
            result.append({
                "target_slug": m.group(1).strip(),
                "relation_type": m.group(2),
                "confidence": float(m.group(3)),
            })
    return result


# ── 站点生成 ──────────────────────────────────────


def generate_site_data(vault_path: Path) -> int:
    """扫描 vault 并生成 site-data.json + 复制静态文件。

    返回解析的笔记数。
    """
    vault_path = vault_path.resolve()
    notes = scan_vault_notes(vault_path)

    languages: set[str] = set()
    for n in notes:
        if n.get("language"):
            languages.add(n["language"])

    site_data = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stats": {
            "total": len(notes),
            "languages": len(languages),
            "lists": len({n["list_name"] for n in notes}),
        },
        "notes": notes,
    }

    # 写入 site-data.json
    (vault_path / "site-data.json").write_text(
        json.dumps(site_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 复制前端静态文件
    pages_dir = Path(__file__).resolve().parent.parent / "pages"
    for fname in _PAGES_STATIC:
        src = pages_dir / fname
        if src.is_file():
            (vault_path / fname).write_text(
                src.read_text(encoding="utf-8"), encoding="utf-8"
            )

    return len(notes)
