---
repo: xbtlin/ai-berkshire
status: reviewed
language: Python
topics: [ai, ai-agent, anthropic, berkshire-hathaway, charlie-munger, china-stock, claude, claude-code, financial-analysis, fintech, fundamental-analysis, investment, investment-research, llm, mcp, portfolio-management, stock-analysis, stock-market, value-investing, warren-buffett]
relations: [Panniantong/Agent-Reach: SIMILAR_TOPICS(1.0), 1jehuang/jcode: SIMILAR_TOPICS(1.0), Canner/WrenAI: SIMILAR_TOPICS(0.8), Canner/WrenAI: ALTERNATIVE(0.5), AstrBotDevs/AstrBot: SIMILAR_TOPICS(1.0), AstrBotDevs/AstrBot: ALTERNATIVE(0.5), KnockOutEZ/wigolo: SIMILAR_TOPICS(1.0), tirth8205/code-review-graph: SIMILAR_TOPICS(1.0), tirth8205/code-review-graph: ALTERNATIVE(0.5), bojieli/ai-agent-book: SIMILAR_TOPICS(1.0), bojieli/ai-agent-book: ALTERNATIVE(0.5), affaan-m/ECC: SIMILAR_TOPICS(1.0), Graphify-Labs/graphify: SIMILAR_TOPICS(1.0), Graphify-Labs/graphify: ALTERNATIVE(0.5), Shubhamsaboo/awesome-llm-apps: ALTERNATIVE(0.5), OpenBB-finance/OpenBB: ALTERNATIVE(0.5), iOfficeAI/OfficeCLI: SIMILAR_TOPICS(0.8), MadsLorentzen/ai-job-search: SIMILAR_TOPICS(0.8), CoplayDev/unity-mcp: SIMILAR_TOPICS(1.0), harvard-edge/cs249r_book: ALTERNATIVE(0.5), Zackriya-Solutions/meetily: SIMILAR_TOPICS(0.8), JuliusBrussee/caveman: SIMILAR_TOPICS(1.0), roboflow/supervision: ALTERNATIVE(0.5), diegosouzapw/OmniRoute: SIMILAR_TOPICS(1.0), HKUDS/Vibe-Trading: SIMILAR_TOPICS(1.0), HKUDS/Vibe-Trading: ALTERNATIVE(0.5), DeusData/codebase-memory-mcp: SIMILAR_TOPICS(0.8), alibaba/page-agent: SIMILAR_TOPICS(0.8), ZhuLinsen/daily_stock_analysis: SIMILAR_TOPICS(0.8), ZhuLinsen/daily_stock_analysis: ALTERNATIVE(0.5), calesthio/OpenMontage: SIMILAR_TOPICS(0.8), xorbitsai/inference: ALTERNATIVE(0.5), sierra-research/tau2-bench: SIMILAR_TOPICS(0.8), sierra-research/tau2-bench: ALTERNATIVE(0.5), langchain-ai/langchain: SIMILAR_TOPICS(1.0), langchain-ai/langchain: ALTERNATIVE(0.5), punkpeye/awesome-mcp-servers: SIMILAR_TOPICS(0.8), modelscope/ms-swift: ALTERNATIVE(0.5), langgenius/dify: SIMILAR_TOPICS(1.0)]
ai_generated: false
human_edited: true
category: tool
rating: 5
maintenance: active
ai_tags: [ai, value-investing, fintech, multi-agent, fundamental-analysis, claude, stock-analysis]
summary: |-
  AI 价值投资研究框架（1.5 万 star，MIT，活跃）：巴菲特/芒格/段永平/李录四大师方法论 + 多 Agent 对抗分析（裁判 Agent 模式），反偏见机制 + 数据校验，实盘验证跑赢主要指数。
  
  **对你（trade-pulse 量化主线）的定位：多 Agent 对抗验证的参考实现。** 核心借鉴点：决策门引入对抗验证（多信号一致才执行）、冲突时暂缓/降仓的裁判机制。与 Vibe-Trading、Kronos、OpenBB、daily_stock_analysis 组成量化工具链。
---

# ai-berkshire

AI 时代的伯克希尔：基于 Claude Code / Codex 的价值投资研究框架。巴菲特·芒格·段永平·李录四大师方法论 + 多Agent并行研究。| AI-era Berkshire: a value investing research framework built for Claude Code / Codex. 4 masters' methodologies + multi-agent adversarial analysis.


## ✦ 人工摘要

AI 价值投资研究框架（1.5 万 star，MIT，活跃）：巴菲特/芒格/段永平/李录四大师方法论 + 多 Agent 对抗分析（裁判 Agent 模式），反偏见机制 + 数据校验，实盘验证跑赢主要指数。

**对你（trade-pulse 量化主线）的定位：多 Agent 对抗验证的参考实现。** 核心借鉴点：决策门引入对抗验证（多信号一致才执行）、冲突时暂缓/降仓的裁判机制。与 Vibe-Trading、Kronos、OpenBB、daily_stock_analysis 组成量化工具链。


## TODO

### P3 — 多 Agent 对抗分析（借鉴其模式）
- [ ] 在 trade-pulse 决策门中实现对抗验证：规则信号 vs Kronos 预测方向一致才执行
- [ ] 信号冲突时设计暂缓/降仓规则（参考 ai-berkshire 的裁判 Agent 模式）


## 评估

**分类**: tool
**评分**: 5/5
**维护状态**: active
**标签**: ai, value-investing, fintech, multi-agent, fundamental-analysis, claude, stock-analysis
