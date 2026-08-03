"""项目工具箱：tables/*.yaml 的读写、join 与校验。

每个文件一张表（一个项目），表内列出仓库及其角色/用途/使用频率。
这是「仓库 × 项目」多对多映射层：一个仓库可出现在多张表，
表内行顺序即展示顺序（不做唯一性约束）。

目录约定：tables/ 与 vault/ 平级（vault_path.parent / "tables"）。
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# ── 合法取值 ──────────────────────────────────────────────

ROLES: tuple[str, ...] = ("核心", "辅助", "候选")
USAGES: tuple[str, ...] = ("daily", "weekly", "rare")
STATUSES: tuple[str, ...] = ("active", "paused", "archived")

DEFAULT_ROLE = "候选"
DEFAULT_USAGE = "rare"
DEFAULT_STATUS = "active"


# ── 异常 ──────────────────────────────────────────────


class TableError(Exception):
    """表文件读取/解析失败。"""


# ── 数据模型 ──────────────────────────────────────────────


@dataclass
class RepoRow:
    """表内一行：一个仓库及其角色/用途/备注。"""

    repo: str
    role: str = DEFAULT_ROLE
    usage: str = DEFAULT_USAGE
    note: str = ""

    def to_dict(self) -> dict:
        """序列化为 YAML 字典（保持字段顺序）。"""
        return {
            "repo": self.repo,
            "role": self.role,
            "usage": self.usage,
            "note": self.note,
        }


@dataclass
class TableData:
    """一张项目表。"""

    project: str
    title: str = ""
    purpose: str = ""
    status: str = DEFAULT_STATUS
    repos: list[RepoRow] = field(default_factory=list)
    path: Path | None = None  # 来源文件（保存后回填）

    def to_dict(self) -> dict:
        """序列化为 YAML 字典（保持字段顺序）。"""
        return {
            "project": self.project,
            "title": self.title,
            "purpose": self.purpose,
            "status": self.status,
            "repos": [r.to_dict() for r in self.repos],
        }


# ── 工具函数 ──────────────────────────────────────────────


def tables_dir(vault_path: Path) -> Path:
    """tables/ 与 vault/ 平级：<vault 父目录>/tables。"""
    return vault_path.resolve().parent / "tables"


def repo_to_slug(repo: str) -> str:
    """'owner/name' → 'owner.name'（小写）；无 owner 的纯 name 原样返回。"""
    return repo.replace("/", ".").lower()


# ── 读取/写入 ──────────────────────────────────────────────


def load_tables(vault_path: Path) -> list[TableData]:
    """扫描 tables/*.yaml，按文件名顺序返回全部表。

    单个文件损坏时抛 TableError（带文件名上下文），便于 CLI 报错定位。
    """
    tdir = tables_dir(vault_path)
    if not tdir.is_dir():
        return []
    tables: list[TableData] = []
    for f in sorted(tdir.glob("*.yaml")):
        tables.append(load_table_file(f))
    return tables


def load_table_file(path: Path) -> TableData:
    """读取单张表文件。"""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        raise TableError(f"表文件 YAML 解析失败: {path}: {e}") from e
    if not isinstance(raw, dict):
        raise TableError(f"表文件顶层应为映射（dict）: {path}")

    project = str(raw.get("project") or path.stem)
    repos: list[RepoRow] = []
    for item in raw.get("repos") or []:
        if not isinstance(item, dict):
            continue
        repo_name = str(item.get("repo") or "").strip()
        if not repo_name:
            continue
        repos.append(
            RepoRow(
                repo=repo_name,
                role=str(item.get("role") or DEFAULT_ROLE),
                usage=str(item.get("usage") or DEFAULT_USAGE),
                note=str(item.get("note") or ""),
            )
        )

    return TableData(
        project=project,
        title=str(raw.get("title") or ""),
        purpose=str(raw.get("purpose") or ""),
        status=str(raw.get("status") or DEFAULT_STATUS),
        repos=repos,
        path=path,
    )


def load_table(vault_path: Path, project: str) -> TableData | None:
    """按 project 查找单张表，不存在返回 None。"""
    for t in load_tables(vault_path):
        if t.project == project:
            return t
    return None


def _scalar(value: str) -> str:
    """YAML 标量输出：安全字符裸写，否则双引号转义。

    json.dumps 的双引号形式是合法 YAML 标量，可处理冒号/井号等特殊字符。
    """
    if value and not _SAFE_SCALAR_RE.match(value):
        return json.dumps(value, ensure_ascii=False)
    return value


_SAFE_SCALAR_RE = re.compile(r"^[\w \-./·：，、（）%+]+$")


def _dump_table(table: TableData) -> str:
    """表 → YAML 文本，字段顺序与行顺序稳定（与手写格式一致）。"""
    lines = [
        f"project: {_scalar(table.project)}",
        f"title: {_scalar(table.title)}",
        f"purpose: {_scalar(table.purpose)}",
        f"status: {_scalar(table.status)}",
        "repos:",
    ]
    for row in table.repos:
        lines.append(f"  - repo: {_scalar(row.repo)}")
        lines.append(f"    role: {_scalar(row.role)}")
        lines.append(f"    usage: {_scalar(row.usage)}")
        lines.append(f"    note: {_scalar(row.note)}")
    return "\n".join(lines) + "\n"


def save_table(table: TableData, vault_path: Path) -> Path:
    """写回 tables/<project>.yaml（自动建目录），返回文件路径。"""
    tdir = tables_dir(vault_path)
    tdir.mkdir(parents=True, exist_ok=True)
    path = tdir / f"{table.project}.yaml"
    path.write_text(_dump_table(table), encoding="utf-8")
    table.path = path
    return path


def delete_table(table: TableData, vault_path: Path) -> None:
    """删除表文件（rm 删空表 --force 用）。"""
    path = table.path or tables_dir(vault_path) / f"{table.project}.yaml"
    if path.is_file():
        path.unlink()


# ── join vault 元数据（B3）────────────────────────────────


def join_table(table: TableData, notes_index: dict[str, dict]) -> dict:
    """表 → site-data 结构：每行 repo join vault 笔记元数据。

    参数：
        table: 表数据
        notes_index: {slug: note_dict}，slug 为 'owner.name' 小写
            （由 scan_vault_notes() 结果构建）

    返回 dict 结构见任务书 B3：join 字段 vault 有则填、无则 null。
    """
    rows: list[dict] = []
    for row in table.repos:
        note = None
        if "/" in row.repo:  # 有 owner 才尝试匹配本地 vault
            note = notes_index.get(repo_to_slug(row.repo))
        rows.append(
            {
                "repo": row.repo,
                "role": row.role,
                "usage": row.usage,
                "note": row.note,
                # join 字段（vault 有则填，无则 null）
                "slug": note["slug"] if note else None,
                "language": note["language"] if note else None,
                "stars": None,  # vault 笔记不采集 star 数，统一 null
                "summary": note["ai_summary"] if note else None,
                "list_name": note["list_name"] if note else None,
                "collected": note is not None,
            }
        )
    return {
        "project": table.project,
        "title": table.title,
        "purpose": table.purpose,
        "status": table.status,
        "repos": rows,
    }


# ── 一致性校验（B2 validate）────────────────────────────────


def validate_tables(
    vault_path: Path,
    notes_index: dict[str, dict] | None = None,
) -> tuple[list[str], list[str]]:
    """一致性检查，返回 (warnings, errors)。

    - warning: repo 不在本地 vault → 未收录（候选仓库，允许存在）
    - error:   同一表内重复行 / 未知 role / 未知 usage
    """
    if notes_index is None:
        from star_vault.core.pages import scan_vault_notes

        notes_index = {n["slug"]: n for n in scan_vault_notes(vault_path)}

    warnings: list[str] = []
    errors: list[str] = []
    tables = load_tables(vault_path)

    for t in tables:
        label = f"{t.project} ({t.path.name if t.path else t.project + '.yaml'})"
        seen: set[str] = set()
        for row in t.repos:
            slug = repo_to_slug(row.repo)
            if "/" not in row.repo:
                warnings.append(
                    f"[{label}] {row.repo}: 无 owner，视为未收录（候选）"
                )
            elif slug not in notes_index:
                warnings.append(
                    f"[{label}] {row.repo}: 未收录（不在本地 vault，候选）"
                )
            if slug in seen:
                errors.append(f"[{label}] {row.repo}: 重复行（同一表内重复）")
            seen.add(slug)
            if row.role not in ROLES:
                errors.append(
                    f"[{label}] {row.repo}: 未知 role={row.role!r}"
                    f"（合法值: {'/'.join(ROLES)}）"
                )
            if row.usage not in USAGES:
                errors.append(
                    f"[{label}] {row.repo}: 未知 usage={row.usage!r}"
                    f"（合法值: {'/'.join(USAGES)}）"
                )

    return warnings, errors
