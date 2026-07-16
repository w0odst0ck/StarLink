"""配置加载与安全管理。

支持多数据源：内置默认值 → star-vault.yaml → 环境变量。
token 自动脱敏，空 token 启动即报错。
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

# ── 自定义异常 ──────────────────────────────────────────────


class ConfigError(Exception):
    """配置加载失败。"""


# ── 配置子模型 ──────────────────────────────────────────────


class GitHubConfig(BaseModel):
    """GitHub API 配置。"""

    token: str = ""
    base_url: str = "https://api.github.com"


class VaultConfig(BaseModel):
    """Vault 路径与行为配置。"""

    path: str = "./vault"
    initial_sync_limit: int = 50
    include_archived: bool = False
    exclude_forks: bool = True


class RelationsConfig(BaseModel):
    """关系引擎配置。"""

    engine: str = "builtin"
    min_confidence: float = 0.3


class AIConfig(BaseModel):
    """AI 分析配置。"""

    provider: str = "openai"
    model: str = "gpt-4o-mini"
    api_key: str = ""
    base_url: str = ""
    max_tokens: int = 512
    temperature: float = 0.3
    max_workers: int = 3
    skip_on_error: bool = True


class StateConfig(BaseModel):
    """状态文件配置。"""

    path: str = ".star-vault-state.json"


# ── 根配置 ──────────────────────────────────────────────────


class Config(BaseModel):
    """全局配置根模型。"""

    github: GitHubConfig = Field(default_factory=GitHubConfig)
    vault: VaultConfig = Field(default_factory=VaultConfig)
    relations: RelationsConfig = Field(default_factory=RelationsConfig)
    ai: AIConfig = Field(default_factory=AIConfig)
    state: StateConfig = Field(default_factory=StateConfig)

    def dump_safe(self, indent: int = 2) -> str:
        """输出脱敏后的配置 JSON，不暴露 token。"""
        raw = self.model_dump()
        raw["github"]["token"] = _mask(raw["github"]["token"])
        raw["ai"]["api_key"] = _mask(raw["ai"]["api_key"])
        return json_dumps(raw, indent=indent)

    def __repr__(self) -> str:
        return self.dump_safe()


# ── 工具函数 ──────────────────────────────────────────────


def _mask(value: str) -> str:
    """脱敏：保留首 3 尾 2，中间变 *。

    >>> _mask("abc123def")
    'abc****ef'
    >>> _mask("ab")
    '****'
    >>> _mask("")
    ''
    """
    if not value:
        return ""
    if len(value) <= 5:
        return "****"
    return value[:3] + "****" + value[-2:]


def json_dumps(obj: Any, indent: int = 2) -> str:
    """JSON 序列化，支持 datetime。"""
    import json as _json
    from datetime import datetime as _dt

    def _serializer(o: Any) -> str:
        if isinstance(o, _dt):
            return o.isoformat()
        raise TypeError(f"Object of type {type(o)} is not JSON serializable")

    return _json.dumps(obj, default=_serializer, indent=indent, ensure_ascii=False)


_ENV_MAP: dict[str, str] = {
    "github.token": "GH_TOKEN",
    "ai.api_key": "OPENAI_API_KEY",
    "ai.base_url": "OPENAI_BASE_URL",
    "ai.model": "AI_MODEL",
    "vault.path": "VAULT_PATH",
}


def _resolve_env_path(env_var: str) -> str | None:
    """获取环境变量值，Tilde 展开（支持 ~/path）。"""
    val = os.environ.get(env_var)
    if val is None:
        return None
    return str(Path(val).expanduser())


def _set_nested(cfg: Config, dotted_key: str, value: str) -> None:
    """按点分路径设置配置属性，不抛异常。"""
    parts = dotted_key.split(".")
    obj = cfg
    for part in parts[:-1]:
        obj = getattr(obj, part, None)
        if obj is None:
            return
    setattr(obj, parts[-1], value)


def find_config(
    explicit: str | None = None,
    cwd: Path | None = None,
) -> Path | None:
    """搜索配置文件路径。

    优先级：
      1. --config 显式指定
      2. CWD 下的 star-vault.yaml

    参数：
        explicit: 用户通过 CLI --config 传入的路径
        cwd: 当前工作目录（单元测试注入用）
    """
    if explicit:
        p = Path(explicit).expanduser()
        if p.is_file():
            return p
        raise ConfigError(f"指定的配置文件不存在: {explicit}")

    cwd = cwd or Path.cwd()
    local = cwd / "star-vault.yaml"
    if local.is_file():
        return local

    return None


def _merge_env(config: Config) -> None:
    """用环境变量覆盖已有配置值。"""
    for dotted_key, env_var in _ENV_MAP.items():
        val = _resolve_env_path(env_var) if env_var == "VAULT_PATH" else os.environ.get(env_var)
        if val is not None:
            _set_nested(config, dotted_key, val)


# ── 主入口 ──────────────────────────────────────────────


def load_config(config_path: str | None = None) -> Config:
    """加载配置。

    优先级（降序）：
      环境变量 > star-vault.yaml > 内置默认值

    抛出：
        ConfigError: token 为空时
    """
    cfg = Config()

    # 1. 加载 YAML 配置覆盖
    found = find_config(explicit=config_path)
    if found:
        import yaml

        raw = yaml.safe_load(found.read_text(encoding="utf-8")) or {}
        _apply_yaml(cfg, raw)

    # 2. 环境变量覆盖（最高优先级）
    _merge_env(cfg)

    # 3. 空 token 零容忍
    if not cfg.github.token:
        raise ConfigError(
            "GitHub token 未设置。请设置环境变量 GH_TOKEN 或在 star-vault.yaml 中配置 github.token"
        )

    return cfg


def _apply_yaml(cfg: Config, raw: dict) -> None:
    """将 YAML 配置递归应用到 Config 对象。"""
    if "github" in raw:
        if "token" in raw["github"]:
            cfg.github.token = str(raw["github"]["token"])
        if "base_url" in raw["github"]:
            cfg.github.base_url = str(raw["github"]["base_url"])
    if "vault" in raw:
        if "path" in raw["vault"]:
            cfg.vault.path = str(raw["vault"]["path"])
        if "initial_sync_limit" in raw["vault"]:
            cfg.vault.initial_sync_limit = int(raw["vault"]["initial_sync_limit"])
        if "include_archived" in raw["vault"]:
            cfg.vault.include_archived = bool(raw["vault"]["include_archived"])
        if "exclude_forks" in raw["vault"]:
            cfg.vault.exclude_forks = bool(raw["vault"]["exclude_forks"])
    if "relations" in raw:
        if "engine" in raw["relations"]:
            cfg.relations.engine = str(raw["relations"]["engine"])
        if "min_confidence" in raw["relations"]:
            cfg.relations.min_confidence = float(raw["relations"]["min_confidence"])
    if "ai" in raw:
        if "api_key" in raw["ai"]:
            cfg.ai.api_key = str(raw["ai"]["api_key"])
        if "model" in raw["ai"]:
            cfg.ai.model = str(raw["ai"]["model"])
        if "base_url" in raw["ai"]:
            cfg.ai.base_url = str(raw["ai"]["base_url"])
        if "max_tokens" in raw["ai"]:
            cfg.ai.max_tokens = int(raw["ai"]["max_tokens"])
        if "temperature" in raw["ai"]:
            cfg.ai.temperature = float(raw["ai"]["temperature"])
        if "max_workers" in raw["ai"]:
            cfg.ai.max_workers = int(raw["ai"]["max_workers"])
        if "skip_on_error" in raw["ai"]:
            cfg.ai.skip_on_error = bool(raw["ai"]["skip_on_error"])
        if "provider" in raw["ai"]:
            cfg.ai.provider = str(raw["ai"]["provider"])
    if "state" in raw:
        if "path" in raw["state"]:
            cfg.state.path = str(raw["state"]["path"])
