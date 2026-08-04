"""GitHub Pages 站点数据生成。

scan_vault_notes() 扫描 vault/stars/ 目录，解析全部笔记 markdown 文件，
产出 site-data.json 供前端 SPA 使用。

用法：
    star-vault sync --with-pages    # 同步后生成页面
    star-vault pages                # 从已有 vault 重新生成
"""

from __future__ import annotations

import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path

from star_vault.core.tables import build_tables_data, load_tables

logger = logging.getLogger(__name__)

_PAGES_STATIC = ("index.html", "app.js", "style.css", "graph.js")

# ── 扫描 vault ──────────────────────────────────────


def scan_vault_notes(vault_path: Path) -> list[dict]:
    """扫描 vault/stars/ 下所有 .md 笔记，返回结构化数据列表。"""
    stars_dir = vault_path / "stars"
    if not stars_dir.is_dir():
        return []

    notes: list[dict] = []
    seen: dict[str, Path] = {}
    for md_file in sorted(stars_dir.rglob("*.md")):
        if md_file.stem in seen:
            # 兜底：重复 slug 报警并跳过，避免脏数据进 site-data
            logger.warning(
                "重复笔记 slug=%s: %s 与 %s 并存（建议清理，可先跑 sync 收敛）",
                md_file.stem,
                seen[md_file.stem],
                md_file,
            )
            continue
        seen[md_file.stem] = md_file
        note = _parse_note_file(md_file)
        if note:
            notes.append(note)

    return notes


def _parse_note_file(path: Path) -> dict | None:
    """解析单篇笔记 markdown 文件。"""
    content = path.read_text(encoding="utf-8")

    # 解析 frontmatter（--- 块）
    fm = _parse_frontmatter(content)

    # 提取 body 中的结构化内容
    body = _parse_body(content)

    # 摘要优先级：frontmatter summary > 正文 ✦ 摘要段
    summary = (fm.get("summary") or "").strip() if fm else ""
    if not summary:
        summary = body.get("ai_summary", "")

    # 即使没有 frontmatter 也返回带默认值的笔记数据
    return {
        "slug": path.stem,
        "title": body.get("title", path.stem),
        "repo_full_name": fm.get("repo", "") if fm else "",
        "list_name": path.parent.name,
        "language": (fm.get("language") or "") or None if fm else None,
        "topics": fm.get("topics", []) if fm else [],
        "status": fm.get("status", "unreviewed") if fm else "unreviewed",
        "ai_generated": fm.get("ai_generated", False) if fm else False,
        "ai_summary": summary,
        "todo_items": body.get("todo_items", []),
        "relations": _parse_relations(fm.get("relations", [])) if fm else [],
        # AI 增强字段 (v2)
        "category": fm.get("category", "") if fm else "",
        "rating": _safe_int(fm.get("rating", 0)) if fm else 0,
        "maintenance": fm.get("maintenance", "") if fm else "",
        "ai_tags": fm.get("ai_tags", []) if fm else [],
        # 项目工具箱归属 (v3)：人工在笔记 frontmatter 维护
        "toolboxes": _parse_str_list(fm.get("toolboxes")) if fm else [],
    }


def _parse_str_list(value: object) -> list[str]:
    """解析 frontmatter 字符串列表字段，兼容多种形式。"""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        s = value.strip()
        if s.startswith("[") and s.endswith("]"):
            inner = s[1:-1].strip()
            return [x.strip().strip('"\'') for x in inner.split(",") if x.strip()]
        return [s] if s else []
    return []


def _safe_int(value: object, default: int = 0) -> int:
    """安全转 int，非数值返回默认值。"""
    try:
        return int(value)  # type: ignore[arg-type]
    except (ValueError, TypeError):
        return default


def _parse_frontmatter(content: str) -> dict:
    """解析 --- 分隔的 frontmatter（支持 YAML 块标量）。"""
    m = re.match(r"^---\n(.+?)\n---(?:\n|$)", content, re.DOTALL)
    if not m:
        return {}

    try:
        import yaml

        data = yaml.safe_load(m.group(1)) or {}
        if isinstance(data, dict):
            return data
    except yaml.YAMLError as e:
        # frontmatter 不是合法 YAML 时回退旧解析器，但记录问题便于排查
        print(f"[warn] frontmatter YAML 解析失败，回退逐行解析: {e}")
    except Exception as e:
        print(f"[warn] frontmatter 解析异常，回退逐行解析: {e}")

    # 回退：逐行解析（兼容非标准格式）
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
            result[key] = [x.strip().strip('"') for x in inner.split(",")] if inner else []
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

    # 摘要：## ✦ AI 摘要 / ✦ 人工摘要 后直到下一个 ## 或结尾
    summary_m = re.search(r"## ✦ (?:AI 摘要|人工摘要)\n\n(.+?)(?=\n## |\Z)", body, re.DOTALL)
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
    """解析 frontmatter relations: target_slug: TYPE(confidence)

    兼容两种形式：
      - YAML 解析后的 dict 列表：[{owner/name: TYPE(conf)}, ...]
      - 字符串列表：["owner/name: TYPE(conf)", ...]
    """
    result: list[dict] = []
    for rel in rels:
        if isinstance(rel, dict):
            # dict 形式：{target: "TYPE(conf)"}
            for target, spec in rel.items():
                m = re.match(r"(\w+)\(([\d.]+)\)", str(spec))
                if m:
                    result.append({
                        "target_slug": str(target).strip(),
                        "relation_type": m.group(1),
                        "confidence": float(m.group(2)),
                    })
        elif isinstance(rel, str):
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
    if not vault_path.is_dir():
        raise NotADirectoryError(f"Vault 路径不存在或不是目录: {vault_path}")
    notes = scan_vault_notes(vault_path)

    languages: set[str] = set()
    for n in notes:
        if n.get("language"):
            languages.add(n["language"])

    # 项目工具箱：两源合一（表配置 + 笔记 toolboxes 声明）
    notes_index = {n["slug"]: n for n in notes}
    tables_data = build_tables_data(load_tables(vault_path), notes_index)

    site_data = {
        "version": 3,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stats": {
            "total": len(notes),
            "languages": len(languages),
            "lists": len({n["list_name"] for n in notes}),
            "tables": len(tables_data),
        },
        "notes": notes,
        "tables": tables_data,
    }

    # 写入 site-data.json
    (vault_path / "site-data.json").write_text(
        json.dumps(site_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return len(notes)
