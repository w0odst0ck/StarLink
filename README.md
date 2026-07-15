# StarLink

> GitHub Stars → 结构化知识库 × AI 摘要 × 关系图谱

StarLink 把你的 GitHub starred repositories 同步为一个有结构的 Markdown vault。每个仓库自动生成 **AI 摘要** 和 **TODO 项**，并通过可插拔的关系引擎发现项目间的隐性关联。

适合拥有大量 stars（50+）但从未系统梳理过的开发者。

---

## 快速开始

```bash
# 安装
pip install star-vault

# 配置
export GH_TOKEN="ghp_xxx"

# 同步（首次，拉最近 50 个）
star-vault sync --limit 50

# 进入你的知识库
cd ./vault
```

> ⚠️ **隐私提醒**：配置完成后请运行 `git status`，确认 `star-vault.yaml`、`.env`、`plan/`、`memory/` 等敏感目录未出现在待提交列表中。

## 配置

| 环境变量 | 用途 | 默认值 |
|---------|------|--------|
| `GH_TOKEN` | GitHub Personal Access Token | 必填 |
| `OPENAI_API_KEY` | AI API 密钥 | 可选（跳过 AI） |
| `AI_MODEL` | AI 模型 | `gpt-4o-mini` |
| `VAULT_PATH` | vault 目录 | `./vault` |

或创建 `star-vault.yaml` 进行精细配置。

## 架构

```
GitHub API ──→ Syncer ──→ Vault Manager ──→ Markdown Vault
                    │                            │
                    ├── Relation Engine           ├── INDEX.md
                    │    ├── builtin (规则)       ├── TODO.md
                    │    └── AI (高级)            └── relations/
                    │
                    └── AI Pipeline
                         ├── 摘要生成
                         └── TODO 生成
```

## 路线图

| 阶段 | 内容 | 状态 |
|------|------|------|
| Phase 0 | 原型：核心同步链路 + 规则引擎 + AI 摘要 | 🚧 规划中 |
| Phase 1 | MVP：增量同步 + AI 验证 + 交互式 review | 📋 待定 |
| Phase 2 | 增强：图谱可视化 + 社区引擎 + 多 provider | 🔮 远期 |

详见 [`plan/`](plan/)。

## 项目结构

```
StarLink/
├── star_vault/             # Python 包
│   ├── models/             # 数据模型
│   ├── core/               # 核心逻辑（同步、vault、索引）
│   ├── relations/          # 关系引擎
│   ├── ai/                 # AI 客户端 + prompts
│   └── templates/          # Jinja2 模板
├── plan/                   # 项目规划
│   ├── roadmap.md          # 全局路线图
│   ├── phase0.md           # Phase 0 任务分解
│   └── design/             # 详细设计文档
└── memory/                 # 开发日志
```

## 许可

MIT
