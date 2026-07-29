"""StarLink CLI: sync, status, config 命令。

入口点（pyproject.toml）：
    star-vault = "star_vault.core.cli:app"
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

import typer

from star_vault import __version__
import hashlib

from star_vault.core.config import ConfigError, load_config
from star_vault.core.syncer import sync as sync_repos
from star_vault.core.state import AI_STATUS_DONE, AI_STATUS_FAILED, AI_STATUS_LOCKED, AI_STATUS_PENDING, StateManager
from star_vault.core.vault import build_note, write_note
from star_vault.core.index_generator import render_vault_index, render_todo_index
from star_vault.core.pages import generate_site_data, scan_vault_notes
from star_vault.models.note import NoteData, TodoItem
from star_vault.models.relation import RelationRef

def _prompt_version() -> str:
    """返回当前 AI prompt 版本 hash（用于 stale 检测）。"""
    prompt_dir = Path(__file__).resolve().parent.parent / "ai" / "prompts"
    hasher = hashlib.sha256()
    for f in sorted(prompt_dir.glob("*.txt")):
        hasher.update(f.read_bytes())
    return hasher.hexdigest()[:12]


app = typer.Typer(
    name="star-vault",
    help="GitHub Stars → structured Markdown knowledge vault",
    no_args_is_help=True,
)


@app.command()
def sync(
    mode: str = typer.Option("full", "--mode", "-m", help="full | incremental"),
    limit: int | None = typer.Option(
        None, "--limit", "-n", help="最大同步仓库数（默认无限制）"
    ),
    no_relations: bool = typer.Option(
        False, "--no-relations", help="跳过关系分析"
    ),
    no_ai: bool = typer.Option(
        False, "--no-ai", help="跳过 AI 分析（需配置 OPENAI_API_KEY）"
    ),
    with_pages: bool = typer.Option(
        False, "--with-pages", help="同步后生成 GitHub Pages 静态站点"
    ),
    ai_only: bool = typer.Option(
        False, "--ai-only", help="仅重新运行 AI 分析，不重新同步"
    ),
):
    """同步 GitHub stars 到本地 vault。"""
    config = load_config()
    vault_path = Path(config.vault.path).expanduser().resolve()

    # 1. 同步
    all_repos: list = []
    if ai_only:
        typer.echo("AI-only 模式：跳过同步步骤，从 vault 读取已有数据…")
        vault_path = Path(config.vault.path).expanduser().resolve()
        from star_vault.models.repo import RepoData

        state_path = vault_path / config.state.path
        if not state_path.is_file():
            typer.echo("✗ 没有 vault 状态数据，请先运行: star-vault sync")
            raise typer.Exit(1)

        prompt_key = _prompt_version()
        sm = StateManager(vault_path, state_relpath=config.state.path)
        state = sm.load()
        raw_state = json.loads(state_path.read_text(encoding="utf-8"))

        skipped_locked = 0
        skipped_done = 0
        for full_name, repo_state in raw_state.get("repos", {}).items():
            if not sm.needs_reanalysis(full_name, prompt_key):
                # 检查 human_edited
                slug = full_name.replace("/", ".").lower()
                note_path = vault_path / "stars" / repo_state.get("list_name", "_uncategorized") / f"{slug}.md"
                if note_path.is_file():
                    content = note_path.read_text(encoding="utf-8")
                    if "human_edited: true" in content:
                        skipped_locked += 1
                        continue
                skipped_done += 1
                continue

            owner, name = full_name.split("/", 1)
            all_repos.append(RepoData(
                owner=owner, name=name,
                full_name=full_name,
                description=repo_state.get("description", ""),
                topics=repo_state.get("topics", []),
                language=repo_state.get("language", ""),
                list_name=repo_state.get("list_name", "uncategorized"),
                html_url=repo_state.get("html_url", f"https://github.com/{full_name}"),
                starred_at=repo_state.get("starred_at", ""),
                readme_snippet=repo_state.get("readme_snippet", ""),
            ))
        typer.echo(
            f"  需分析 {len(all_repos)}, "
            f"跳过 {skipped_done}（已分析）, "
            f"锁定 {skipped_locked}（人工编辑）"
        )
        if not all_repos:
            typer.echo("✓ 所有 repo 均已分析，无需处理")
            return
    else:
        typer.echo("正在同步 GitHub stars…")
        result = sync_repos(config, mode=mode, limit=limit)
        typer.echo(
            f"  新增 {len(result.new_repos)}, 更新 {len(result.updated_repos)}, "
            f"未变 {result.unchanged_count}"
        )
        all_repos = result.new_repos + result.updated_repos + result.ai_pending
        if not all_repos:
            typer.echo("⚠  没有需要处理的 repo")
            return

    # 2. 关系分析（可选）
    relations_map: dict[str, list] = {}
    if not no_relations:
        typer.echo("正在分析关系…")
        from star_vault.relations.base import EngineHub
        from star_vault.models.relation import RelationRef

        EngineHub.load_builtin()
        engine = EngineHub.get("builtin")

        for repo in all_repos:
            rels = engine.analyze_repo(repo, all_repos)
            relations_map[repo.full_name] = [
                RelationRef(
                    target_slug=r.target,
                    relation_type=r.relation_type,
                    confidence=r.confidence,
                )
                for r in rels
            ]

    # 3. AI 分析（可选）
    ai_results: dict[str, dict] = {}
    if not no_ai:
        typer.echo("正在 AI 分析…")
        from star_vault.ai.client import AIClient
        from star_vault.models.note import TodoItem

        client = AIClient(
            api_key=config.ai.api_key or os.environ.get("OPENAI_API_KEY", ""),
            gh_token=config.github.token,
            base_url=config.ai.base_url or os.environ.get("OPENAI_BASE_URL", ""),
            model=config.ai.model or os.environ.get("AI_MODEL", "gpt-4o-mini"),
        )

        sm = StateManager(vault_path, state_relpath=config.state.path)
        state = sm.load()

        prompt_key = _prompt_version()
        analysis = client.analyze_batch(all_repos)
        for repo in all_repos:
            if r := analysis.get(repo.full_name):
                ai_results[repo.full_name] = {
                    "summary": r.summary,
                    "todos": [TodoItem(text=t, source_repo=repo.full_name) for t in r.todos],
                    "category": r.category,
                    "rating": r.rating,
                    "maintenance": r.maintenance,
                    "tags": r.tags,
                }
            # 标记状态
            existing = sm.get_repo(repo.full_name)
            if existing is None:
                continue
            existing.readme_fetched = True
            has_result = repo.full_name in analysis and bool(analysis[repo.full_name].summary)
            existing.ai_status = AI_STATUS_DONE if has_result else AI_STATUS_FAILED
            existing.ai_cache_key = prompt_key
            sm.upsert_repo(repo.full_name, existing)
        sm.save()

    # 4. 写入 vault
    typer.echo("写入 vault…")
    notes = []
    for repo in all_repos:
        kwargs = {"relations": relations_map.get(repo.full_name)}
        if ai_res := ai_results.get(repo.full_name):
            kwargs["ai_summary"] = ai_res["summary"]
            kwargs["ai_generated"] = bool(ai_res["summary"])
            kwargs["todo_items"] = ai_res.get("todos", [])
            kwargs["category"] = ai_res.get("category", "")
            kwargs["rating"] = ai_res.get("rating", 0)
            kwargs["maintenance"] = ai_res.get("maintenance", "")
            kwargs["ai_tags"] = ai_res.get("tags", [])
        note = build_note(repo, **kwargs)
        write_note(note, vault_path)
        notes.append(note)

    # 5. Pages（可选）
    page_count = 0
    if with_pages:
        typer.echo("\n正在生成 Pages 站点…")
        page_count = generate_site_data(vault_path)

    # summary
    typer.echo(f"\n✓ Vault: {vault_path}")
    typer.echo(f"  ├─ {len(notes)} 篇笔记")
    typer.echo(f"")
    typer.echo(f"💡 重新生成索引: star-vault index")
    if page_count:
        typer.echo(f"  └─ Pages: {page_count} repos → index.html + site-data.json")


@app.command()
def status():
    """显示 vault 状态（含 AI 分析统计）。"""
    config = load_config()
    vault_path = Path(config.vault.path).expanduser().resolve()
    state_path = vault_path / config.state.path

    if not state_path.is_file():
        typer.echo("✗ 还未同步过，请先运行: star-vault sync")
        raise typer.Exit()

    sm = StateManager(vault_path, state_relpath=config.state.path)
    state = sm.load()

    repo_count = len(state.repos)
    last_sync = state.last_sync_at

    # AI 状态统计
    ai_counts: Counter[str] = Counter()
    for rs in state.repos.values():
        status = rs.ai_status or (AI_STATUS_DONE if rs.ai_analyzed else AI_STATUS_PENDING)
        ai_counts[status] += 1

    # 扫描 vault 中的笔记
    note_files = sorted(vault_path.rglob("stars/**/*.md"))
    languages: Counter[str] = Counter()
    for f in note_files:
        content = f.read_text(encoding="utf-8")
        if m := re.search(r"language: (.+)", content):
            lang = m.group(1).strip().strip('"')
            if lang:
                languages[lang] += 1

    typer.echo(f"Vault:  {vault_path}")
    typer.echo(f"上次同步: {last_sync}")
    typer.echo(f"仓库数:  {repo_count}")
    typer.echo(f"笔记数:  {len(note_files)}")
    if languages:
        top5 = dict(languages.most_common(5))
        typer.echo(f"语言分布: {top5}")
    typer.echo(f"")
    typer.echo(f"AI 分析:")
    typer.echo(f"  ├─ 已完成: {ai_counts.get(AI_STATUS_DONE, 0)}")
    typer.echo(f"  ├─ 待分析: {ai_counts.get(AI_STATUS_PENDING, 0)}")
    typer.echo(f"  ├─ 失败:   {ai_counts.get(AI_STATUS_FAILED, 0)}")
    typer.echo(f"  ├─ 已锁定: {ai_counts.get(AI_STATUS_LOCKED, 0)}")
    typer.echo(f"  └─ Prompt版本: {_prompt_version()}")


@app.command()
def config():
    """显示当前配置（脱敏）。"""
    try:
        cfg = load_config()
    except Exception as e:
        typer.echo(f"✗ 配置加载失败: {e}", err=True)
        raise typer.Exit(1) from e

    typer.echo(cfg.dump_safe())


@app.command()
def analyze(
    repo: str = typer.Argument(
        None, help="单 repo 全名（如 owner/repo），不传则按 --failed/--stale 过滤"
    ),
    failed: bool = typer.Option(
        False, "--failed", help="重试所有失败的分析"
    ),
    stale: bool = typer.Option(
        False, "--stale", help="重跑所有 prompt 版本过期的分析"
    ),
    unlock: bool = typer.Option(
        False, "--unlock", help="同时处理 human_edited 的 repo"
    ),
):
    """定点 AI 分析：单仓库 / 重试失败 / 重跑过期。"""
    config = load_config()
    vault_path = Path(config.vault.path).expanduser().resolve()
    state_path = vault_path / config.state.path

    if not state_path.is_file():
        typer.echo("✗ 没有 vault 状态数据")
        raise typer.Exit(1)

    from star_vault.models.repo import RepoData

    sm = StateManager(vault_path, state_relpath=config.state.path)
    state = sm.load()
    prompt_key = _prompt_version()

    # 确定待分析列表
    targets: list[tuple[str, dict]] = []
    raw = json.loads(state_path.read_text(encoding="utf-8"))

    if repo:
        if repo in raw.get("repos", {}):
            targets = [(repo, raw["repos"][repo])]
        else:
            typer.echo(f"✗ 未找到仓库: {repo}")
            raise typer.Exit(1)
    else:
        for full_name, rs in raw.get("repos", {}).items():
            rstatus = rs.get("ai_status", "")
            if failed and rstatus not in (AI_STATUS_FAILED, ""):
                continue
            if stale and rstatus not in (AI_STATUS_STALE, ""):
                continue
            if not unlock:
                slug = full_name.replace("/", ".").lower()
                list_name = rs.get("list_name", "_uncategorized")
                note_path = vault_path / "stars" / list_name / f"{slug}.md"
                if note_path.is_file() and "human_edited: true" in note_path.read_text():
                    continue
            targets.append((full_name, rs))

    if not targets:
        typer.echo("✓ 没有需要分析的 repo")
        return

    typer.echo(f"准备分析 {len(targets)} 个 repo…")

    from star_vault.ai.client import AIClient
    from star_vault.models.note import TodoItem

    client = AIClient(
        api_key=config.ai.api_key or os.environ.get("OPENAI_API_KEY", ""),
        gh_token=config.github.token,
        base_url=config.ai.base_url or os.environ.get("OPENAI_BASE_URL", ""),
        model=config.ai.model or os.environ.get("AI_MODEL", "gpt-4o-mini"),
    )

    repos: list[RepoData] = []
    for full_name, rs in targets:
        owner, name = full_name.split("/", 1)
        repos.append(RepoData(
            owner=owner, name=name,
            full_name=full_name,
            description=rs.get("description", ""),
            topics=rs.get("topics", []),
            language=rs.get("language", ""),
            list_name=rs.get("list_name", "uncategorized"),
            html_url=rs.get("html_url", f"https://github.com/{full_name}"),
            starred_at=rs.get("starred_at", ""),
            readme_snippet=rs.get("readme_snippet", ""),
        ))

    analysis = client.analyze_batch(repos)

    for repo_data in repos:
        r = analysis.get(repo_data.full_name)
        existing = sm.get_repo(repo_data.full_name)

        if r and r.summary:
            existing.ai_status = AI_STATUS_DONE
            existing.ai_cache_key = prompt_key
            typer.echo(f"  ✅ {repo_data.full_name}: {r.rating}/5, {r.category}")
        else:
            existing.ai_status = AI_STATUS_FAILED
            typer.echo(f"  ❌ {repo_data.full_name}: 分析失败")

        existing.readme_fetched = True
        sm.upsert_repo(repo_data.full_name, existing)

        # 写入笔记
        note = build_note(
            repo_data,
            ai_summary=r.summary if r else "",
            ai_generated=bool(r and r.summary),
            todo_items=[TodoItem(text=t, source_repo=repo_data.full_name) for t in (r.todos if r else [])],
            category=r.category if r else "",
            rating=r.rating if r else 0,
            maintenance=r.maintenance if r else "",
            ai_tags=r.tags if r else [],
        )
        write_note(note, vault_path)

    sm.save()
    typer.echo(f"\n✓ {len(repos)} 个 repo 处理完成")
    typer.echo(f"  重新生成 Pages: star-vault pages")


@app.command()
def index(
    vault_dir: str = typer.Option(
        "./vault", "--vault", "-d",
        help="vault 目录路径（默认 ./vault）",
    ),
):
    """从 vault/stars/ 重新生成 INDEX.md + TODO.md。

    不依赖 GitHub Token，不需要网络连接。
    运行于 sync/analyze 之后，确保索引与 vault 笔记一致。
    """
    vault_path: Path
    try:
        cfg = load_config()
        vault_path = Path(cfg.vault.path).expanduser().resolve()
    except ConfigError:
        vault_path = Path(vault_dir).expanduser().resolve()

    stars_dir = vault_path / "stars"
    if not stars_dir.is_dir():
        typer.echo(f"✗ Vault 中未找到笔记数据: {vault_path}")
        typer.echo("请先运行: star-vault sync")
        raise typer.Exit(1)

    typer.echo(f"扫描 Vault: {vault_path}")
    raw_notes = scan_vault_notes(vault_path)
    if not raw_notes:
        typer.echo("✗ vault/stars/ 下无笔记文件")
        raise typer.Exit(1)

    def _to_note(d: dict) -> NoteData:
        todos = [
            TodoItem(
                text=t["text"],
                source_repo=d["repo_full_name"],
                priority=t.get("priority", 3),
                done=t.get("done", False),
            )
            for t in d.get("todo_items", [])
        ]
        relations = [
            RelationRef(
                target_slug=r["target_slug"],
                relation_type=r["relation_type"].lower(),
                confidence=r.get("confidence", 0.5),
            )
            for r in d.get("relations", [])
        ]
        return NoteData(
            slug=d.get("slug", d.get("title", "unknown")),
            title=d.get("title", d.get("slug", "Untitled")),
            repo_full_name=d.get("repo_full_name", ""),
            list_name=d.get("list_name", ""),
            description="",
            language=d.get("language"),
            topics=d.get("topics", []),
            status=d.get("status", "unreviewed"),
            ai_generated=d.get("ai_generated", False),
            ai_summary=d.get("ai_summary", ""),
            todo_items=todos,
            relations=relations,
            category=d.get("category", ""),
            rating=d.get("rating", 0),
            maintenance=d.get("maintenance", ""),
            ai_tags=d.get("ai_tags", []),
        )

    notes = [_to_note(d) for d in raw_notes]

    (vault_path / "INDEX.md").write_text(
        render_vault_index(notes), encoding="utf-8"
    )
    (vault_path / "TODO.md").write_text(
        render_todo_index(notes), encoding="utf-8"
    )

    typer.echo(f"\n✓ 索引已更新")
    typer.echo(f"  ├─ INDEX.md: {len(notes)} 个仓库")
    typer.echo(f"  ├─ TODO.md: {sum(len(n.todo_items) for n in notes)} 项")
    typer.echo(f"  └─ 源: vault/stars/")


@app.command()
def pages(
    vault_dir: str = typer.Option(
        "./vault", "--vault", "-d",
        help="vault 目录路径（默认 ./vault；可通过 star-vault.yaml 的 vault.path 配置）",
    ),
):
    """从已有 vault 数据重新生成 Pages 站点。

    不依赖 GitHub Token，不需要网络连接。
    """
    # 有配置则优先用配置的 vault.path，无需 token 的配置项仍可加载
    vault_path: Path
    try:
        cfg = load_config()
        vault_path = Path(cfg.vault.path).expanduser().resolve()
    except ConfigError:
        vault_path = Path(vault_dir).expanduser().resolve()

    if not (vault_path / "stars").is_dir():
        typer.echo(f"✗ Vault 中未找到笔记数据: {vault_path}")
        typer.echo("请先运行: star-vault sync")
        raise typer.Exit(1)

    typer.echo(f"扫描 Vault: {vault_path}")
    count = generate_site_data(vault_path)
    typer.echo(f"\n✓ Pages 站点已生成")
    typer.echo(f"  ├─ {count} 篇笔记")
    typer.echo(f"  ├─ site-data.json")
    typer.echo(f"  ├─ index.html")
    typer.echo(f"  ├─ app.js")
    typer.echo(f"  └─ style.css")
    typer.echo(f"\n下一步：将 {vault_path} 部署到 GitHub Pages，或运行 star-vault sync --with-pages")


if __name__ == "__main__":
    app()
