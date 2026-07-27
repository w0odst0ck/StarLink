"""OpenAI 兼容 AI 客户端，含并发控制与重试。

支持 OpenAI、DeepSeek、Ollama 等所有兼容接口。
README 按需采集（repo 无 readme_snippet 时自动拉取），智能截取。
"""

from __future__ import annotations

import base64
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx
from openai import OpenAI

from star_vault.models.repo import RepoData

logger = logging.getLogger(__name__)

_TEMPLATE_DIR = Path(__file__).resolve().parent / "prompts"
_PROMPT_V1: str | None = None
_PROMPT_V2: str | None = None

_MAX_README_CHARS = 4000  # README 智能截取上限
_MAX_TOKENS = 3072  # AI 响应最大 token 数（v2 输出更长）
_MAX_RETRIES = 1  # 失败自动重试次数


# ── 分级章节标题（遇到就截断）─────────────────────────


_STOP_SECTIONS = (
    "## installation", "## install", "## getting started",
    "## quick start", "## quickstart", "## setup", "## usage",
    "## api", "## configuration", "## contributing",
)


# ── 分析结果数据类 ──────────────────────────────────


@dataclass
class AnalysisResult:
    """单次 AI 分析的结果（v2，含分类/评分/标签）。"""

    summary: str = ""
    todos: list[str] = field(default_factory=list)
    category: str = ""
    rating: int = 0
    maintenance: str = ""
    tags: list[str] = field(default_factory=list)


# ── AI 客户端 ──────────────────────────────────────


class AIClient:
    """AI 分析客户端。

    自动按需采集 README（需要 gh_token）。
    支持 v1/v2 两种 prompt 版本，默认为 v2。
    """

    def __init__(
        self,
        api_key: str,
        gh_token: str = "",
        base_url: str = "",
        model: str = "gpt-4o-mini",
        max_workers: int = 3,
    ) -> None:
        self._client = OpenAI(api_key=api_key, base_url=base_url or None)
        self._gh_token = gh_token
        self._model = model
        self._max_workers = max_workers

    # ── 公共接口 ────────────────────────────────────────────

    def analyze(self, repo: RepoData, prompt_version: str = "v2") -> AnalysisResult:
        """对单个 repo 执行 AI 分析，失败自动重试。"""
        last_error: Exception | None = None
        for attempt in range(_MAX_RETRIES + 1):
            try:
                self._ensure_readme(repo)
                system_msg, prompt = self._build_messages(repo, prompt_version)
                resp = self._client.chat.completions.create(
                    model=self._model,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=_MAX_TOKENS,
                    temperature=0.3,
                )
                return self._parse_response(resp, prompt_version)
            except Exception as e:
                last_error = e
                if attempt < _MAX_RETRIES:
                    logger.debug("AI 分析重试 [%s] attempt %d: %s", repo.full_name, attempt + 1, e)

        logger.warning("AI 分析失败 [%s]: %s", repo.full_name, last_error)
        return AnalysisResult()

    def analyze_batch(
        self, repos: list[RepoData], prompt_version: str = "v2"
    ) -> dict[str, AnalysisResult]:
        """批量分析，线程池控制并发。"""
        from concurrent.futures import ThreadPoolExecutor, as_completed

        results: dict[str, AnalysisResult] = {}
        with ThreadPoolExecutor(max_workers=self._max_workers) as pool:
            fut_map = {
                pool.submit(self.analyze, r, prompt_version): r.full_name for r in repos
            }
            for fut in as_completed(fut_map):
                name = fut_map[fut]
                try:
                    results[name] = fut.result()
                except Exception as e:
                    logger.warning("AI 分析异常 [%s]: %s", name, e)
                    results[name] = AnalysisResult()
        return results

    # ── README 按需采集 ─────────────────────────────────────

    def _ensure_readme(self, repo: RepoData) -> None:
        """如果 repo 没有 README 内容，从 GitHub API 拉取。"""
        if repo.readme_snippet or not self._gh_token:
            return

        try:
            url = f"https://api.github.com/repos/{repo.full_name}/readme"
            headers = {
                "Authorization": f"Bearer {self._gh_token}",
                "Accept": "application/vnd.github.v3.raw+json",
                "User-Agent": "StarLink/0.1",
            }
            resp = httpx.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                content_b64 = data.get("content", "")
                if data.get("encoding") == "base64" and content_b64:
                    decoded = base64.b64decode(content_b64).decode(
                        "utf-8", errors="replace"
                    )
                    repo.readme_snippet = self._smart_truncate(decoded)
                else:
                    repo.readme_snippet = ""
            else:
                logger.debug("README 404 [%s]", repo.full_name)
                repo.readme_snippet = ""
        except Exception as e:
            logger.debug("README 采集失败 [%s]: %s", repo.full_name, e)
            repo.readme_snippet = ""

    @staticmethod
    def _smart_truncate(text: str, max_chars: int = _MAX_README_CHARS) -> str:
        """智能截取 README：在章节标题处截止，避免腰斩内容。"""
        if len(text) <= max_chars:
            return text

        # 前 max_chars 字符内查找最近的停靠章节标题
        head = text[:max_chars].lower()
        best_pos = max_chars
        for section in _STOP_SECTIONS:
            pos = head.rfind(section)
            if pos != -1 and pos < best_pos:
                best_pos = pos

        return text[:best_pos].rstrip() + "\n\n..."

    # ── Prompt 构建 ────────────────────────────────────────

    @classmethod
    def _build_messages(cls, repo: RepoData, prompt_version: str) -> tuple[str, str]:
        """构建 system + user 消息。返回 (system_prompt, user_prompt)。"""
        global _PROMPT_V1, _PROMPT_V2

        if prompt_version == "v2":
            if _PROMPT_V2 is None:
                tmpl_path = _TEMPLATE_DIR / "repo_analysis_v2.txt"
                _PROMPT_V2 = tmpl_path.read_text(encoding="utf-8")
            # v2 的 system role 已内嵌在 prompt template 中
            system = "You are StarLink AI Analyst, an expert at evaluating GitHub repositories."
            user_prompt = _PROMPT_V2
        else:
            if _PROMPT_V1 is None:
                tmpl_path = _TEMPLATE_DIR / "repo_analysis_v1.txt"
                _PROMPT_V1 = tmpl_path.read_text(encoding="utf-8")
            system = "You are a helpful assistant."
            user_prompt = _PROMPT_V1

        readme = repo.readme_snippet or "(无 README)"
        user_prompt = user_prompt.format(
            owner=repo.owner,
            name=repo.name,
            description=repo.description or "(无描述)",
            topics=", ".join(repo.topics) if repo.topics else "(无标签)",
            language=repo.language or "Unknown",
            readme=readme,
        )

        return system, user_prompt

    # ── 响应解析 ────────────────────────────────────────────

    @staticmethod
    def _parse_response(resp: Any, prompt_version: str) -> AnalysisResult:
        """解析 AI 响应。"""
        content = resp.choices[0].message.content or ""
        content = content.strip()

        # 提取最外层 {...} 区域
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end > start:
            json_str = content[start : end + 1]
        else:
            json_str = content

        # 去掉 markdown code block
        json_str = (
            json_str.removeprefix("```json")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )

        # 解析 JSON，兼容 Extra data
        data: dict | None = None
        parse_err: str | None = None
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            parse_err = str(e)
            if "Extra data" in parse_err:
                end_brace = json_str.find("}")
                if end_brace != -1:
                    try:
                        data = json.loads(json_str[: end_brace + 1])
                    except json.JSONDecodeError:
                        pass

        if data is None:
            logger.warning(
                "AI 响应 JSON 解析失败: %s | content: %.80s",
                parse_err or "unknown",
                json_str,
            )
            return AnalysisResult()

        if prompt_version == "v2":
            # v2.1 todos 可能是 [{"text":"...","urgency":1}] 或 ["..."]
            todos_raw = data.get("todos", [])
            todos: list[str] = []
            for t in todos_raw:
                if isinstance(t, dict):
                    todos.append(str(t.get("text", t.get("urgency", ""))))
                else:
                    todos.append(str(t))
            return AnalysisResult(
                summary=data.get("summary", ""),
                todos=todos,
                category=str(data.get("category", "")),
                rating=int(data.get("rating", 0)),
                maintenance=str(data.get("maintenance", "")),
                tags=data.get("tags", []),
            )

        # v1 兼容：todos 可能是 ["..."] 或 [{"text":"..."}]
        todos_raw = data.get("todos", [])
        todos = [str(t.get("text", t)) if isinstance(t, dict) else str(t) for t in todos_raw]
        return AnalysisResult(
            summary=data.get("summary", ""),
            todos=todos,
        )
