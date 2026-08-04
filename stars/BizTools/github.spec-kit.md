---
repo: github/spec-kit
status: reviewed
language: Python
topics: [ai, copilot, development, engineering, prd, spec, spec-driven]
relations: [CoplayDev/unity-mcp: SIMILAR_TOPICS(0.8), calesthio/OpenMontage: SIMILAR_TOPICS(0.8)]
ai_generated: false
human_edited: true
category: tool
rating: 4
maintenance: active
ai_tags: [spec-driven-development, cli, python, ai, copilot]
toolboxes: [indiestore]
summary: |-
  GitHub 官方的规范驱动开发（SDD）工具包（12.5 万 star，MIT，活跃）。`specify` CLI 生成标准化流程：constitution（项目原则）→ specify（需求，只讲 what/why）→ plan（技术方案）→ tasks（任务拆解）→ taskstoissues（转 GitHub issues）→ implement（AI 执行）→ converge（对照 spec 检查）。支持 30+ AI agent（Claude Code/Codex/Cursor 等）。
  
  **对你（AI 开发流程）的价值：不是项目管理工具，是「AI 开发流程规范化」工具。** 核心思想「先写清楚要什么再让 AI 实现」与你的习惯（项目先写计划.md）同源，但把流程标准化、可执行化——解决 AI 开发没章法的问题。⚠️ **OpenClaw 不在官方支持列表**：适配方案 = spec-kit 生成 spec/plan/tasks 文档（本质 markdown），OpenClaw 读文档执行任务，即「spec-kit 管流程定义，OpenClaw 管执行」。任务跟踪/进度管理它帮不上（不是看板），靠 GitHub Issues/项目文档。
---

# spec-kit

💫 Toolkit to help you get started with Spec-Driven Development


## ✦ 人工摘要

GitHub 官方的规范驱动开发（SDD）工具包（12.5 万 star，MIT，活跃）。`specify` CLI 生成标准化流程：constitution（项目原则）→ specify（需求，只讲 what/why）→ plan（技术方案）→ tasks（任务拆解）→ taskstoissues（转 GitHub issues）→ implement（AI 执行）→ converge（对照 spec 检查）。支持 30+ AI agent（Claude Code/Codex/Cursor 等）。

**对你（AI 开发流程）的价值：不是项目管理工具，是「AI 开发流程规范化」工具。** 核心思想「先写清楚要什么再让 AI 实现」与你的习惯（项目先写计划.md）同源，但把流程标准化、可执行化——解决 AI 开发没章法的问题。⚠️ **OpenClaw 不在官方支持列表**：适配方案 = spec-kit 生成 spec/plan/tasks 文档（本质 markdown），OpenClaw 读文档执行任务，即「spec-kit 管流程定义，OpenClaw 管执行」。任务跟踪/进度管理它帮不上（不是看板），靠 GitHub Issues/项目文档。


## TODO


- [ ] 在下一个项目（trade-pulse 新功能 / 独立站模块）试用 SDD 流程：先写 spec → plan → tasks，再开发 (P2)

- [ ] 评估适配方案：specify CLI 生成文档 + OpenClaw 读文档执行，记录适配成本 (P3)

- [ ] 学其流程设计（constitution/specify/plan/tasks 拆分粒度），沉淀自己的 AI 开发流程规范 (P3)




## 评估

**分类**: tool
**评分**: 4/5
**维护状态**: active
**标签**: spec-driven-development, cli, python, ai, copilot
