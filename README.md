# StarLink ✦

> GitHub Stars → 结构化知识库 × AI 摘要 × 关系图谱

StarLink 把你的 GitHub starred repositories 同步为一个有结构的 Markdown vault。每个仓库自动生成 **AI 摘要**、**分类评分** 和 **TODO 项**，并通过关系引擎发现项目间的隐性关联。

---

🌐 **在线看板**：[https://w0odst0ck.github.io/StarLink/](https://w0odst0ck.github.io/StarLink/)

---

## 快速开始

```bash
# 安装
pip install star-vault

# 配置（GitHub Token 需要 public_repo 权限）
export GH_TOKEN="ghp_xxx"

# 同步所有 stars
star-vault sync

# 打开知识库
cd ./vault
```

> ⚠️ **隐私提醒**：`star-vault.yaml`、`.env`、`plan/`、`memory/`、`vault/` 已配置在 `.gitignore` 中，不会被提交。

---

## 进阶用法

```bash
# 首次先拉 10 个试试
star-vault sync --limit 10 --no-relations

# 全量同步（含 AI 分析，需配置 API Key）
star-vault sync

# 只重新跑 AI 分析，不重新拉取
star-vault sync --ai-only

# 查看状态
star-vault status
```

| 命令 | 用途 |
|------|------|
| `star-vault sync` | 全量同步 + AI 分析 + 关系分析 |
| `star-vault sync --ai-only` | 仅重新 AI 分析 |
| `star-vault sync --no-relations` | 跳过关系分析 |
| `star-vault status` | 查看 vault 统计 |
| `star-vault pages` | 从已有 vault 生成 Pages 站点 |

---

## 许可

MIT
