---
repo: alibaba/open-code-review
status: reviewed
language: Go
topics: [agent, agent-skills, code-review, code-review-assistant, harness, repository-level-context]
relations: []
ai_generated: false
human_edited: true
category: tool
rating: 5
maintenance: active
ai_tags: [code-review, llm, agent, go, alibaba]
toolboxes: [starlink-self, agent-learning]
summary: |-
  阿里开源的 AI 代码审查 CLI（1.7 万 star，Apache 2.0，活跃）。混合架构：确定性规则管道 + LLM Agent，行级审查意见，内置微调规则集（NPE、线程安全、XSS、SQL 注入），OpenAI/Anthropic 兼容。
  
  **对你：已在用的日常工具。** 你的工作流就是「提交前跑 `ocr review`（全局 npm 包，配 DeepSeek）→ 修 high/medium → 再交付」。不用评估"要不要用"，而是**吃透它的审查能力边界**：内置规则集覆盖哪些坑、LLM 审查在什么场景会漏，把它的审查维度对接自己的项目踩坑记录。
---

# open-code-review

Open-source & free — Battle-tested at Alibaba's scale. Hybrid architecture code review tool: deterministic pipelines + LLM Agent, precise line-level comments, built-in fine-tuned ruleset (NPE, thread-safety, XSS, SQL injection), OpenAI & Anthropic compatible.


## ✦ 人工摘要

阿里开源的 AI 代码审查 CLI（1.7 万 star，Apache 2.0，活跃）。混合架构：确定性规则管道 + LLM Agent，行级审查意见，内置微调规则集（NPE、线程安全、XSS、SQL 注入），OpenAI/Anthropic 兼容。

**对你：已在用的日常工具。** 你的工作流就是「提交前跑 `ocr review`（全局 npm 包，配 DeepSeek）→ 修 high/medium → 再交付」。不用评估"要不要用"，而是**吃透它的审查能力边界**：内置规则集覆盖哪些坑、LLM 审查在什么场景会漏，把它的审查维度对接自己的项目踩坑记录。


## TODO


- [ ] 梳理内置规则集覆盖的检查项（NPE/线程安全/XSS/SQL 注入等），对照自己项目的常见 bug 类型 (P2)

- [ ] 记录 ocr review 在真实项目上的漏报/误报案例，沉淀自己的审查补充清单 (P2)

- [ ] 评估提示词/规则定制空间，看能否把 trade-pulse 等项目的专属检查项加进去 (P3)




## 评估

**分类**: tool
**评分**: 5/5
**维护状态**: active
**标签**: code-review, llm, agent, go, alibaba
