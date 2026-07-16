"""OpenAI 兼容 AI 客户端，含并发控制与重试。

支持 OpenAI、DeepSeek、Ollama 等所有兼容接口。
不依赖 response_format=json_object（兼容所有后端）。
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openai import OpenAI

from star_vault.models.repo import RepoData

logger = logging.getLogger(__name__)

_TEMPLATE_DIR = Path(__file__).resolve().parent / "prompts"
_PROMPT_TEMPLATE: str | None = None


@dataclass
class AnalysisResult:
    """单次 AI 分析的结果。"""

    summary: str
    todos: list[str]


class AIClient:
    """AI 分析客户端。

    用法：
        client = AIClient(api_key="sk-xxx", base_url="https://api.deepseek.com/v1")
        result = client.analyze(repo)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "",
        model: str = "gpt-4o-mini",
        max_workers: int = 3,
    ) -> None:
        self._client = OpenAI(api_key=api_key, base_url=base_url or None)
        self._model = model

    # ── 公共接口 ────────────────────────────────────────────

    def analyze(self, repo: RepoData) -> AnalysisResult:
        """对单个 repo 执行 AI 分析。

        如果分析失败（网络/解析/模型异常），返回空结果并记日志。
        """
        try:
            prompt = self._get_prompt(repo)
            resp = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
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

    # ── 内部 ────────────────────────────────────────────────

    @classmethod
    def _get_prompt(cls, repo: RepoData) -> str:
        """加载 Prompt 模板并填充 repo 数据。

        模板文件类级缓存，避免重复读盘。
        """
        global _PROMPT_TEMPLATE
        if _PROMPT_TEMPLATE is None:
            tmpl_path = _TEMPLATE_DIR / "repo_analysis_v1.txt"
            _PROMPT_TEMPLATE = tmpl_path.read_text(encoding="utf-8")

        return _PROMPT_TEMPLATE.format(
            owner=repo.owner,
            name=repo.name,
            description=repo.description or "(无描述)",
            topics=", ".join(repo.topics) if repo.topics else "(无标签)",
            language=repo.language or "Unknown",
            readme_snippet=repo.readme_snippet[:500] or "(无 README)",
        )

    @staticmethod
    def _parse_response(resp: Any) -> AnalysisResult:
        """解析 AI 响应，处理各种非标准格式。"""
        content = resp.choices[0].message.content or ""
        content = content.strip()

        # 1) 尝试提取最外层 {...} 区域
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end > start:
            json_str = content[start : end + 1]
        else:
            json_str = content

        # 2) 去掉 markdown code block 包裹
        json_str = (
            json_str.removeprefix("```json")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )

        # 3) 尝试解析 JSON
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            logger.warning("AI 响应 JSON 解析失败: %s", json_str[:120])
            return AnalysisResult(summary="", todos=[])

        return AnalysisResult(
            summary=data.get("summary", ""),
            todos=data.get("todos", []),
        )
