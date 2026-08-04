#!/usr/bin/env python3
"""按 toolbox-map.yaml 批量写入笔记 frontmatter toolboxes 字段。

设计（2026-08-04 方案 B）：
    - 笔记是归属真相（人工可改）；映射文件只是批量初始化/维护工具
    - 幂等：已有 toolboxes 的仓库跳过写入，绝不覆盖人工已定归属
    - --report 对账：输出「映射有/笔记无」与「笔记有/映射无」差异，
      用于人工精修后检查映射文件是否过期

用法：
    python scripts/apply_toolbox_map.py            # 批量写入（幂等）
    python scripts/apply_toolbox_map.py --report   # 只对账不写入
    python scripts/apply_toolbox_map.py --dry-run  # 预览改动
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

from star_vault.core.vault import slug_from_full_name

BACKUP_ROOT = Path.home() / "backups"
MAP_PATH = Path(__file__).resolve().parent / "toolbox-map.yaml"


def _is_human_protected(content: str) -> bool:
    """与 vault.py 一致：human_edited 或 frontmatter toolboxes 视为人工内容。"""
    if "human_edited: true" in content:
        return True
    if content.startswith("---\n"):
        end = content.find("\n---", 4)
        if end != -1 and "toolboxes:" in content[4:end]:
            return True
    return False


def _find_note(vault_path: Path, slug: str) -> Path | None:
    """全库查找同 slug 笔记文件（锚点语义：多副本时优先人工版，歧义跳过）。"""
    stars_root = vault_path / "stars"
    if not stars_root.is_dir():
        return None
    hits = [p for p in stars_root.rglob("*.md") if p.stem == slug]
    if not hits:
        return None
    if len(hits) == 1:
        return hits[0]
    protected = [p for p in hits if _is_human_protected(p.read_text(encoding="utf-8"))]
    if len(protected) == 1:
        return protected[0]
    print(f"  ! {slug}: {len(hits)} 个副本且无法判定锚点，跳过")
    return None


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


def _set_toolboxes(fm_text: str, toolboxes: list[str]) -> str:
    """行级替换/插入 toolboxes 行（不整体重序列化，避免破坏 summary: |- 块标量）。"""
    line = f"toolboxes: [{', '.join(toolboxes)}]"
    lines = fm_text.split("\n")
    for i, l in enumerate(lines):
        if l.startswith("toolboxes:"):
            lines[i] = line
            return "\n".join(lines) + "\n"
    # 不存在：ai_tags 行后插入（无则插 summary 前，再无则末尾）
    insert_at = None
    for i, l in enumerate(lines):
        if l.startswith("ai_tags:"):
            insert_at = i + 1
            break
    if insert_at is None:
        for i, l in enumerate(lines):
            if l.startswith("summary:"):
                insert_at = i
                break
    if insert_at is None:
        insert_at = len(lines)
    lines.insert(insert_at, line)
    return "\n".join(lines) + "\n"


def load_map() -> tuple[dict[str, dict], dict[str, str]]:
    """读映射文件 → (toolbox 元信息, repo→toolbox)。"""
    raw = yaml.safe_load(MAP_PATH.read_text(encoding="utf-8")) or {}
    meta: dict[str, dict] = {}
    repo_tb: dict[str, str] = {}
    for tb, cfg in raw.items():
        meta[tb] = {"title": cfg.get("title", tb), "purpose": cfg.get("purpose", "")}
        for repo in cfg.get("repos", []):
            repo_tb[repo.lower()] = tb
    return meta, repo_tb


def apply(vault_path: Path, *, dry_run: bool = False) -> None:
    meta, repo_tb = load_map()
    changes: list[tuple[Path, str]] = []
    total = 0

    for repo, tb in sorted(repo_tb.items()):
        slug = slug_from_full_name(repo)
        note_path = _find_note(vault_path, slug)
        if note_path is None:
            print(f"  ○ {repo}: 本地无笔记，跳过")
            continue
        total += 1
        content = note_path.read_text(encoding="utf-8")
        fm, fm_text, body = _read_frontmatter(content)
        cur = [str(x).strip() for x in (fm.get("toolboxes") or []) if str(x).strip()]
        if tb in cur:
            continue  # 已归属，不覆盖
        new_list = cur + [tb]
        new_fm = _set_toolboxes(fm_text, new_list)
        new_content = f"---\n{new_fm}---{body}"
        if new_content == content:
            continue
        changes.append((note_path, new_content))
        action = "+" if not cur else "~"
        print(f"  {action} {repo} → toolboxes: [{', '.join(new_list)}]")

    if dry_run:
        print(f"\n[dry-run] 将改动 {len(changes)} 个文件（{total} 个仓库检查），未写入")
        return
    if not changes:
        print(f"无改动（{total} 个仓库检查完毕，幂等）")
        return

    backup_dir = BACKUP_ROOT / f"starlink-toolboxmap-{datetime.now():%Y%m%d}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    for path, _ in changes:
        shutil.copy2(path, backup_dir / path.name)
    for path, new_content in changes:
        path.write_text(new_content, encoding="utf-8")
    print(f"\n✓ 更新 {len(changes)} 个笔记（备份: {backup_dir}）")


def report(vault_path: Path) -> None:
    """对账：映射文件 vs 笔记实际归属。"""
    meta, repo_tb = load_map()
    notes_tb: dict[str, list[str]] = {}
    for f in (vault_path / "stars").rglob("*.md"):
        content = f.read_text(encoding="utf-8")
        fm, _, _ = _read_frontmatter(content)
        tbs = [str(x).strip() for x in (fm.get("toolboxes") or []) if str(x).strip()]
        if tbs:
            notes_tb[f.stem] = tbs

    print("=== 映射有 / 笔记无（映射文件过期，可重跑脚本）===")
    n = 0
    for repo, tb in sorted(repo_tb.items()):
        slug = slug_from_full_name(repo)
        if slug not in notes_tb or tb not in notes_tb[slug]:
            print(f"  {repo} → 应属 {tb}")
            n += 1
    if not n:
        print("  （无）")

    print("\n=== 笔记有 / 映射无（人工新增归属，映射文件待补）===")
    n = 0
    for slug, tbs in sorted(notes_tb.items()):
        for tb in tbs:
            mapped = any(repo_tb.get(slug.replace(".", "/")) == tb for _ in [0])
            if not mapped:
                print(f"  {slug} → {tb}")
                n += 1
    if not n:
        print("  （无）")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", action="store_true", help="只对账不写入")
    parser.add_argument("--dry-run", action="store_true", help="预览改动不写入")
    parser.add_argument(
        "--vault", type=Path, default=None, help="vault 路径（默认 ../vault）"
    )
    args = parser.parse_args()

    vault_path = args.vault or (Path(__file__).resolve().parent.parent / "vault")
    vault_path = vault_path.resolve()
    if args.report:
        report(vault_path)
    else:
        apply(vault_path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
