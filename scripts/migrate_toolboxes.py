#!/usr/bin/env python3
"""存量迁移：tables/*.yaml 的归属 → 笔记 frontmatter toolboxes 字段。

背景（2026-08-04 方案 B）：
    工具箱归属改为「笔记 frontmatter 声明」为主，表保留角色配置。
    本脚本把现有表里的 repo 归属回写到对应笔记，一次性迁移。

行为：
    - 读 tables/*.yaml，对每行 repo 找到对应笔记 vault/stars/**/<slug>.md
    - 笔记 frontmatter 无 toolboxes 字段 → 插入 toolboxes: [project]
    - 已有 toolboxes → 合并去重（幂等，可重复跑）
    - 备份所有改动文件到 --backup-dir（默认 ~/backups/starlink-toolboxes-<date>/）
    - --dry-run 只报告不动文件

用法：
    cd <StarLink 项目根>
    python scripts/migrate_toolboxes.py            # 实际迁移
    python scripts/migrate_toolboxes.py --dry-run  # 预览
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

# 允许从项目根直接跑（不依赖安装）
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

from star_vault.core.tables import load_tables
from star_vault.core.vault import slug_from_full_name

BACKUP_ROOT = Path.home() / "backups"


def _find_note(vault_path: Path, slug: str) -> Path | None:
    """全库查找同 slug 笔记文件。"""
    stars_root = vault_path / "stars"
    if not stars_root.is_dir():
        return None
    hits = [p for p in stars_root.rglob("*.md") if p.stem == slug]
    return hits[0] if hits else None


def _read_frontmatter(content: str) -> tuple[dict, str, str]:
    """解析 frontmatter，返回 (字段 dict, frontmatter 原文, 正文)。"""
    if not content.startswith("---\n"):
        return {}, "", content
    end = content.find("\n---", 4)
    if end == -1:
        return {}, "", content
    fm_text = content[4:end]
    try:
        data = yaml.safe_load(fm_text) or {}
        if not isinstance(data, dict):
            data = {}
    except yaml.YAMLError:
        data = {}
    return data, fm_text, content[end + 4 :]


def _rebuild_frontmatter(data: dict, fm_text: str) -> str:
    """重建 frontmatter 文本。

    优先保留原格式：若原文本无 toolboxes 行，在 ai_tags 行后插入；
    否则用 yaml 重新序列化（字段顺序按 data 键序）。
    """
    toolboxes_line = f"toolboxes: [{', '.join(data['toolboxes'])}]"
    if "toolboxes:" in fm_text:
        # 已存在 → 只替换 toolboxes 行，其余行保持原样（避免破坏多行块标量如 summary: |-）
        lines = fm_text.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("toolboxes:"):
                lines[i] = toolboxes_line
                break
        return "\n".join(lines) + "\n"
    # 无 toolboxes → 在 ai_tags 行后插入（保持原格式）
    lines = fm_text.split("\n")
    insert_at = None
    for i, line in enumerate(lines):
        if line.startswith("ai_tags:"):
            insert_at = i + 1
            break
    if insert_at is None:
        # 兜底：插在 summary 之前（若无则插在最后非空行后）
        for i, line in enumerate(lines):
            if line.startswith("summary:"):
                insert_at = i
                break
    if insert_at is None:
        insert_at = len(lines)
    lines.insert(insert_at, toolboxes_line)
    return "\n".join(lines) + "\n"


def migrate(vault_path: Path, *, dry_run: bool = False) -> None:
    """执行迁移。"""
    tables = load_tables(vault_path)
    if not tables:
        print("✗ tables/ 下无表，无需迁移")
        return

    backup_dir = BACKUP_ROOT / f"starlink-toolboxes-{datetime.now():%Y%m%d}"
    changes: list[tuple[Path, str]] = []
    total_rows = 0

    for t in tables:
        for row in t.repos:
            if "/" not in row.repo:
                continue
            total_rows += 1
            slug = slug_from_full_name(row.repo)
            note_path = _find_note(vault_path, slug)
            if note_path is None:
                print(f"  ○ {row.repo}: 本地无笔记，跳过")
                continue
            content = note_path.read_text(encoding="utf-8")
            fm, fm_text, body = _read_frontmatter(content)
            cur = [str(x).strip() for x in (fm.get("toolboxes") or []) if str(x).strip()]
            if t.project in cur:
                print(f"  · {row.repo}: 已声明 {t.project}，跳过")
                continue
            cur.append(t.project)
            fm["toolboxes"] = cur
            new_fm = _rebuild_frontmatter(fm, fm_text)
            new_content = f"---\n{new_fm}---{body}"
            if new_content == content:
                continue
            changes.append((note_path, new_content))
            print(f"  + {row.repo} → toolboxes: [{', '.join(cur)}]")

    if not changes:
        print(f"\n无改动（{total_rows} 行检查完毕，幂等）")
        return

    if dry_run:
        print(f"\n[dry-run] 将改动 {len(changes)} 个文件，未写入")
        return

    backup_dir.mkdir(parents=True, exist_ok=True)
    for path, _ in changes:
        shutil.copy2(path, backup_dir / path.name)
    for path, new_content in changes:
        path.write_text(new_content, encoding="utf-8")

    print(f"\n✓ 迁移完成：{len(changes)} 个笔记已更新")
    print(f"  备份: {backup_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true", help="预览改动，不写文件"
    )
    parser.add_argument(
        "--vault",
        type=Path,
        default=None,
        help="vault 路径（默认：脚本所在目录的 ../vault）",
    )
    args = parser.parse_args()

    vault_path = args.vault or (Path(__file__).resolve().parent.parent / "vault")
    migrate(vault_path.resolve(), dry_run=args.dry_run)


if __name__ == "__main__":
    main()
