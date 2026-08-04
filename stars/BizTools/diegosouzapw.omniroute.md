---
repo: diegosouzapw/OmniRoute
status: reviewed
language: TypeScript
topics: [a2a, ai-agents, ai-gateway, anthropic, claude, claude-code, cline, codex, copilot, cursor, deepseek, free-ai, gemini, kimi, llm-gateway, mcp, openai, openai-proxy, qwen, token-saver]
relations: [Panniantong/Agent-Reach: SIMILAR_TOPICS(1.0), 1jehuang/jcode: SIMILAR_TOPICS(1.0), Canner/WrenAI: SIMILAR_TOPICS(0.8), AstrBotDevs/AstrBot: SIMILAR_TOPICS(1.0), KnockOutEZ/wigolo: SIMILAR_TOPICS(0.8), tirth8205/code-review-graph: SIMILAR_TOPICS(1.0), affaan-m/ECC: SIMILAR_TOPICS(1.0), Graphify-Labs/graphify: SIMILAR_TOPICS(1.0), vxcontrol/pentagi: SIMILAR_TOPICS(1.0), iOfficeAI/OfficeCLI: SIMILAR_TOPICS(0.8), addyosmani/agent-skills: SIMILAR_TOPICS(1.0), MadsLorentzen/ai-job-search: SIMILAR_TOPICS(0.8), CoplayDev/unity-mcp: SIMILAR_TOPICS(1.0), coreyhaines31/marketingskills: SIMILAR_TOPICS(0.8), JuliusBrussee/caveman: SIMILAR_TOPICS(1.0), DeusData/codebase-memory-mcp: SIMILAR_TOPICS(1.0), alibaba/page-agent: SIMILAR_TOPICS(0.8), xbtlin/ai-berkshire: SIMILAR_TOPICS(1.0), calesthio/OpenMontage: SIMILAR_TOPICS(1.0), ollama/ollama: SIMILAR_TOPICS(0.8), langchain-ai/langchain: SIMILAR_TOPICS(1.0), langgenius/dify: SIMILAR_TOPICS(1.0)]
ai_generated: false
human_edited: true
category: tool
rating: 4
maintenance: active
ai_tags: [ai-gateway, llm, openai-proxy, token-saver, auto-fallback]
toolboxes: [efficiency]
summary: |-
  免费 AI 网关（3.6 万 star，MIT，活跃）：一个端点聚合 290+ 供应商（90+ 免费）/500+ 模型，配额感知自动 fallback，RTK+Caveman 压缩省 15-95% token，兼容主流编码工具，MCP/A2A。
  
  **定位：开发省钱工具 + 网关方案参照，商业场景慎用。** 个人开发用免费池省钱可以；但 AI 独立站**不能押注免费池**——配额不稳定、客户数据经第三方有合规风险。商业高可用需求优先自己用 LiteLLM 搭网关（开源可控、同样支持多供应商 fallback）。DeepSeek 直连起步已足够。
---

# OmniRoute

Never stop coding. Free MIT AI gateway: one endpoint, 290+ providers (90+ free), 500+ models — Kimi, Claude, GPT, OpenAI, Gemini, GLM, DeepSeek, MiniMax. Works with Claude Code, Codex, Cursor, OpenCode, Cline & Copilot. Quota-aware auto-fallback, RTK+Caveman compression saves 15-95% tokens, MCP/A2A, Desktop/PWA. Built by 500+ contributors


## ✦ 人工摘要

免费 AI 网关（3.6 万 star，MIT，活跃）：一个端点聚合 290+ 供应商（90+ 免费）/500+ 模型，配额感知自动 fallback，RTK+Caveman 压缩省 15-95% token，兼容主流编码工具，MCP/A2A。

**定位：开发省钱工具 + 网关方案参照，商业场景慎用。** 个人开发用免费池省钱可以；但 AI 独立站**不能押注免费池**——配额不稳定、客户数据经第三方有合规风险。商业高可用需求优先自己用 LiteLLM 搭网关（开源可控、同样支持多供应商 fallback）。DeepSeek 直连起步已足够。


## TODO


- [ ] 个人开发场景：了解其 token 压缩与免费池机制，评估能否降低 OpenClaw 日常 API 成本 (P3)

- [ ] 独立站 AI 功能做高可用时：对比 OmniRoute vs 自建 LiteLLM 网关的可靠性/合规/可控性 (P3)

- [ ] 明确隐私边界：客户数据是否允许经过第三方网关，写入独立站技术决策记录 (P3)




## 评估

**分类**: tool
**评分**: 4/5
**维护状态**: active
**标签**: ai-gateway, llm, openai-proxy, token-saver, auto-fallback
