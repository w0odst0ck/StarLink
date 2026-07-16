"""INDEX.md 与 TODO.md 生成。"""

from __future__ import annotations

from collections import defaultdict

from star_vault.models.note import NoteData, TodoItem


def render_vault_index(notes: list[NoteData]) -> str:
    """生成 INDEX.md：按 list_name 分组索引。

    每条条目：链接 + 语言 + status。
    """
    grouped: dict[str, list[NoteData]] = defaultdict(list)
    for n in notes:
        grouped[n.list_name].append(n)

    lines: list[str] = [
        "# StarLink Vault Index",
        "",
        f"共 {len(notes)} 个仓库",
        "",
    ]

    for list_name in sorted(grouped):
        items = grouped[list_name]
        lines.append(f"## {list_name}")
        for n in sorted(items, key=lambda x: x.slug):
            path = f"stars/{n.list_name}/{n.slug}.md"
            lang = n.language or ""
            info = f" [{lang}]" if lang else ""
            status_mark = " ✅" if n.status == "reviewed" else ""
            lines.append(f"- [{n.repo_full_name}]({path}){info}{status_mark}")
        lines.append("")

    return "\n".join(lines)


def render_todo_index(notes: list[NoteData]) -> str:
    """生成 TODO.md：所有笔记 TODO 汇总，标记来源。

    按 repo_full_name 分组，priority 1-5 标记 P1-P5。
    """
    all_todos: list[tuple[str, TodoItem]] = []
    for n in notes:
        for t in n.todo_items:
            all_todos.append((n.repo_full_name, t))

    if not all_todos:
        return "# StarLink TODO\n\n暂无 TODO 项。\n"

    grouped: dict[str, list[TodoItem]] = defaultdict(list)
    for repo_name, t in all_todos:
        grouped[repo_name].append(t)

    lines: list[str] = [
        "# StarLink TODO",
        f"共 {len(all_todos)} 项",
        "",
    ]

    for repo_name in sorted(grouped):
        lines.append(f"## {repo_name}")
        for t in grouped[repo_name]:
            checkbox = "[x]" if t.done else "[ ]"
            mark = f"(P{t.priority})" if t.priority else ""
            lines.append(f"- {checkbox} {t.text} {mark}".strip())
        lines.append("")

    return "\n".join(lines)
