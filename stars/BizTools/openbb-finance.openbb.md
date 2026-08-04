---
repo: OpenBB-finance/OpenBB
status: reviewed
language: Python
topics: [ai, crypto, derivatives, economics, equity, finance, fixed-income, machine-learning, openbb, options, python, quantitative-finance, stocks]
relations: [microsoft/AI-For-Beginners: SIMILAR_TOPICS(0.8), Canner/WrenAI: ALTERNATIVE(0.5), AstrBotDevs/AstrBot: SIMILAR_TOPICS(0.8), AstrBotDevs/AstrBot: ALTERNATIVE(0.5), tirth8205/code-review-graph: ALTERNATIVE(0.5), bojieli/ai-agent-book: ALTERNATIVE(0.5), Graphify-Labs/graphify: ALTERNATIVE(0.5), Shubhamsaboo/awesome-llm-apps: ALTERNATIVE(0.5), harvard-edge/cs249r_book: ALTERNATIVE(0.5), roboflow/supervision: SIMILAR_TOPICS(0.8), roboflow/supervision: ALTERNATIVE(0.5), HKUDS/Vibe-Trading: SIMILAR_TOPICS(0.8), HKUDS/Vibe-Trading: ALTERNATIVE(0.5), xbtlin/ai-berkshire: ALTERNATIVE(0.5), ZhuLinsen/daily_stock_analysis: ALTERNATIVE(0.5), calesthio/OpenMontage: SIMILAR_TOPICS(0.8), xorbitsai/inference: ALTERNATIVE(0.5), sierra-research/tau2-bench: ALTERNATIVE(0.5), langchain-ai/langchain: SIMILAR_TOPICS(0.8), langchain-ai/langchain: ALTERNATIVE(0.5), modelscope/ms-swift: ALTERNATIVE(0.5), langgenius/dify: SIMILAR_TOPICS(0.8)]
ai_generated: false
human_edited: true
category: tool
rating: 5
maintenance: active
ai_tags: [python, finance, data-integration, quantitative-finance, ai]
toolboxes: [trade-pulse]
summary: |-
  开源统一金融数据平台（7.1 万 star，活跃）：一个接口聚合多源金融数据（股票/期权/加密/宏观/固收），Python SDK + REST API + MCP Server，面向分析师/量化/AI Agent。
  
  **对你（trade-pulse 量化主线）的定位：量化管线的统一数据层。** 多源聚合免去逐源对接，MCP Server 可直接接进 OpenClaw 让 AI 查金融数据。与 Vibe-Trading（回测/执行）、Kronos（分钟线方向）、ai-berkshire、daily_stock_analysis 组成量化工具链。可作为现有免费数据获取方案的升级/补充路径。
---

# OpenBB

Open Data Platform for analysts, quants and AI agents.


## ✦ 人工摘要

开源统一金融数据平台（7.1 万 star，活跃）：一个接口聚合多源金融数据（股票/期权/加密/宏观/固收），Python SDK + REST API + MCP Server，面向分析师/量化/AI Agent。

**对你（trade-pulse 量化主线）的定位：量化管线的统一数据层。** 多源聚合免去逐源对接，MCP Server 可直接接进 OpenClaw 让 AI 查金融数据。与 Vibe-Trading（回测/执行）、Kronos（分钟线方向）、ai-berkshire、daily_stock_analysis 组成量化工具链。可作为现有免费数据获取方案的升级/补充路径。


## TODO


- [ ] 评估接入 trade-pulse：对比 OpenBB 与现有数据源（akshare 类）的覆盖/稳定性，确定数据层方案 (P2)

- [ ] MCP Server 接进 OpenClaw，实测 AI 查询金融数据（588000 行情/宏观指标） (P2)

- [ ] 与 Vibe-Trading 适配器联动：OpenBB 提供数据 → Vibe-Trading 回测 (P3)




## 评估

**分类**: tool
**评分**: 5/5
**维护状态**: active
**标签**: python, finance, data-integration, quantitative-finance, ai
