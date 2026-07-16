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

## 使用教程

### 环境准备

```bash
# 1. 克隆项目
cd ~/workspace/projects/StarLink

# 2. 安装依赖
pip install --break-system-packages -e .

# 3. 配置 GitHub Token
export GH_TOKEN="ghp_***"
```

> GitHub Token 需要 `public_repo` 权限（只读公开仓库）。
> 创建地址：https://github.com/settings/tokens

---

### 首次同步

```bash
# 拉取所有 starred repos
star-vault sync --no-relations
```

或限制数量快速预览：

```bash
# 先拉 10 个看看效果
star-vault sync --limit 10 --no-relations
```

**输出示例：**

```
正在同步 GitHub stars…
  新增 10, 更新 0, 未变 0
写入 vault…

✓ Vault: /home/xxx/workspace/projects/StarLink/vault
  ├─ 10 篇笔记
  ├─ INDEX.md
  └─ TODO.md
```

---

### 查看产出物

```bash
# vault 目录概览
ls vault/stars/_uncategorized/

# 阅读一篇笔记
cat vault/stars/_uncategorized/pallets.flask.md

# 索引页
cat vault/INDEX.md

# 全局 TODO
cat vault/TODO.md
```

**vault 目录结构：**

```
vault/
├── INDEX.md                  # 按分类索引
├── TODO.md                   # 所有仓库的 TODO 汇总
├── .star-vault-state.json    # 同步状态（自动管理）
└── stars/
    └── _uncategorized/       # 笔记存放目录
        ├── owner.repo-a.md
        └── owner.repo-b.md
```

每篇笔记包含：
- **Frontmatter**：repo 名称、语言、topics、关系列表
- **AI 摘要**（需要配置 OpenAI 密钥）
- **TODO 项**
- **关联仓库**（关系引擎标记的相似项目）

---

### 增量同步

有新的 starred repo 后，再次运行 sync 即可：

```bash
star-vault sync --no-relations
```

默认模式为 `incremental`，只拉取上次同步之后新增的 repo。

如需强制重新拉取全部：

```bash
star-vault sync --mode full --no-relations
```

---

### 全部命令

```
star-vault sync [OPTIONS]

选项：
  --mode, -m TEXT       同步模式: full | incremental （默认 full）
  --limit, -n INT       限制同步数量（测试用，默认全部）
  --no-relations        跳过关系分析

star-vault status
  → 显示 vault 统计：仓库数、笔记数、上次同步时间、语言分布

star-vault config
  → 显示当前配置（token 自动脱敏）
```

---

### 关系分析

不传 `--no-relations` 会额外执行关系分析，发现 repo 间的关联：

```bash
star-vault sync --limit 10
```

内置两条规则：

| 规则 | 检测条件 | 关系类型 |
|------|---------|---------|
| TopicOverlapRule | topics 重叠 ≥ 2 个 | SIMILAR_TOPICS |
| LanguageDomainRule | 同语言 + 同领域关键词 | ALTERNATIVE |

关系信息会嵌入笔记的 frontmatter 和「关联仓库」区块中。

---

### 自定义配置

支持通过 `star-vault.yaml` 配置文件覆盖默认行为：

```yaml
# star-vault.yaml
vault:
  path: ~/Documents/my-stars-vault
  initial_sync_limit: 200

relations:
  min_confidence: 0.5
```

配置优先级（低 → 高）：
```
内置默认值 → star-vault.yaml → 环境变量
```

---

### 常见问题

**Q: star-vault: command not found**

```bash
pip install --break-system-packages -e .
```

**Q: 报错 "GitHub token 未设置"**

确认环境变量已设置：

```bash
export GH_TOKEN="ghp_***"
echo $GH_TOKEN  # 应有输出
```

**Q: 为什么只有 10 篇笔记而不是全部？**

第一次运行加了 `--limit 10`，强制全量 sync 即可恢复：

```bash
star-vault sync --mode full --no-relations
```

**Q: README 说支持 AI 摘要，怎么没有？**

AI 模块仍在开发中（Phase 0 末期），需要配置 `OPENAI_API_KEY`。
当前版本的核心链路已通：**GitHub Stars → Markdown Vault → 关系标记**。

---

## 许可

MIT
