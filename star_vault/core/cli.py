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
from star_vault.core.config import load_config
from star_vault.core.syncer import sync as sync_repos
from star_vault.core.vault import build_note, write_note
from star_vault.core.index_generator import render_vault_index, render_todo_index

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
):
    """同步 GitHub stars 到本地 vault。"""
    config = load_config()
    vault_path = Path(config.vault.path).expanduser().resolve()

    # 1. 同步
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
                    target_slug=repo.full_name.replace("/", ".").lower(),
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
        from star_vault.core.state import StateManager

        sm = StateManager(vault_path, state_relpath=config.state.path)
        state = sm.load()

        analysis = client.analyze_batch(all_repos)
        for repo in all_repos:
            if r := analysis.get(repo.full_name):
                ai_results[repo.full_name] = {
                    "summary": r.summary,
                    "todos": [TodoItem(text=t, source_repo=repo.full_name) for t in r.todos],
                }
            # 标记 README 已采集
            existing = sm.get_repo(repo.full_name)
            if existing and not existing.readme_fetched:
                existing.readme_fetched = True
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
        note = build_note(repo, **kwargs)
        write_note(note, vault_path)
        notes.append(note)

    # 5. 索引
    (vault_path / "INDEX.md").write_text(
        render_vault_index(notes), encoding="utf-8"
    )
    (vault_path / "TODO.md").write_text(
        render_todo_index(notes), encoding="utf-8"
    )

    # summary
    typer.echo(f"\n✓ Vault: {vault_path}")
    typer.echo(f"  ├─ {len(notes)} 篇笔记")
    typer.echo(f"  ├─ INDEX.md")
    typer.echo(f"  └─ TODO.md")


@app.command()
def status():
    """显示 vault 状态。"""
    config = load_config()
    vault_path = Path(config.vault.path).expanduser().resolve()
    state_path = vault_path / config.state.path

    if not state_path.is_file():
        typer.echo("✗ 还未同步过，请先运行: star-vault sync")
        raise typer.Exit()

    raw = json.loads(state_path.read_text(encoding="utf-8"))
    repo_count = len(raw.get("repos", {}))
    last_sync = raw.get("last_sync_at", "N/A")

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


@app.command()
def config():
    """显示当前配置（脱敏）。"""
    try:
        cfg = load_config()
    except Exception as e:
        typer.echo(f"✗ 配置加载失败: {e}", err=True)
        raise typer.Exit(1) from e

    typer.echo(cfg.dump_safe())


if __name__ == "__main__":
    app()
