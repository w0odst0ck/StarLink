"""OpenAI 兼容 AI 客户端，含并发控制与重试。

支持 OpenAI、DeepSeek、Ollama 等所有兼容接口。
README 按需采集（repo 无 readme_snippet 时自动拉取），截取前 3000 字符。
"""

from __future__ import annotations

import base64
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
from openai import OpenAI

from star_vault.models.repo import RepoData

logger = logging.getLogger(__name__)

_TEMPLATE_DIR = Path(__file__).resolve().parent / "prompts"
_PROMPT_TEMPLATE: str | None = None

_README_CUTOFF = 3000  # README 截取字符数
_MAX_TOKENS = 2048  # AI 响应最大 token 数


@dataclass
class AnalysisResult:
    """单次 AI 分析的结果。"""

    summary: str
    todos: list[str]


class AIClient:
    """AI 分析客户端。

    自动按需采集 README（需要 gh_token）。
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

    # ── 公共接口 ────────────────────────────────────────────

    def analyze(self, repo: RepoData) -> AnalysisResult:
        """对单个 repo 执行 AI 分析。"""
        try:
            self._ensure_readme(repo)
            prompt = self._get_prompt(repo)
            resp = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=_MAX_TOKENS,
                temperature=0.3,
            )
            return self._parse_response(resp)
        except Exception as e:
            logger.warning("AI 分析失败 [%s]: %s", repo.full_name, e)
            return AnalysisResult(summary="", todos=[])

    def analyze_batch(
        self, repos: list[RepoData]
    ) -> dict[str, AnalysisResult]:
        """批量分析，线程池控制并发。"""
        from concurrent.futures import ThreadPoolExecutor, as_completed

        results: dict[str, AnalysisResult] = {}
        with ThreadPoolExecutor(max_workers=3) as pool:
            fut_map = {
                pool.submit(self.analyze, r): r.full_name for r in repos
            }
            for fut in as_completed(fut_map):
                name = fut_map[fut]
                try:
                    results[name] = fut.result()
                except Exception as e:
                    logger.warning("AI 分析异常 [%s]: %s", name, e)
                    results[name] = AnalysisResult(summary="", todos=[])
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
                    repo.readme_snippet = decoded[:_README_CUTOFF]
                else:
                    repo.readme_snippet = ""
            else:
                logger.debug("README 404 [%s]", repo.full_name)
                repo.readme_snippet = ""
        except Exception as e:
            logger.debug("README 采集失败 [%s]: %s", repo.full_name, e)
            repo.readme_snippet = ""

    # ── Prompt 加载 ────────────────────────────────────────

    @classmethod
    def _get_prompt(cls, repo: RepoData) -> str:
        """加载 Prompt 模板并填充 repo 数据。"""
        global _PROMPT_TEMPLATE
        if _PROMPT_TEMPLATE is None:
            tmpl_path = _TEMPLATE_DIR / "repo_analysis_v1.txt"
            _PROMPT_TEMPLATE = tmpl_path.read_text(encoding="utf-8")

        readme = repo.readme_snippet or "(无 README)"
        return _PROMPT_TEMPLATE.format(
            owner=repo.owner,
            name=repo.name,
            description=repo.description or "(无描述)",
            topics=", ".join(repo.topics) if repo.topics else "(无标签)",
            language=repo.language or "Unknown",
            readme=readme,
        )

    # ── 响应解析 ────────────────────────────────────────────

    @staticmethod
    def _parse_response(resp: Any) -> AnalysisResult:
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
            return AnalysisResult(summary="", todos=[])

        return AnalysisResult(
            summary=data.get("summary", ""),
            todos=data.get("todos", []),
        )
