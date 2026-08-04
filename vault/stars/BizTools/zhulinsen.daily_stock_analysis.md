---
repo: ZhuLinsen/daily_stock_analysis
status: reviewed
language: Python
topics: [a-stock, ai-agent, aigc, llm, quant, quantitative-finance, quantitative-trading]
relations: [1jehuang/jcode: SIMILAR_TOPICS(0.8), Canner/WrenAI: ALTERNATIVE(0.5), AstrBotDevs/AstrBot: ALTERNATIVE(0.5), tirth8205/code-review-graph: ALTERNATIVE(0.5), bojieli/ai-agent-book: SIMILAR_TOPICS(0.8), bojieli/ai-agent-book: ALTERNATIVE(0.5), Graphify-Labs/graphify: ALTERNATIVE(0.5), Shubhamsaboo/awesome-llm-apps: ALTERNATIVE(0.5), OpenBB-finance/OpenBB: ALTERNATIVE(0.5), harvard-edge/cs249r_book: ALTERNATIVE(0.5), roboflow/supervision: ALTERNATIVE(0.5), HKUDS/Vibe-Trading: SIMILAR_TOPICS(1.0), HKUDS/Vibe-Trading: ALTERNATIVE(0.5), xbtlin/ai-berkshire: SIMILAR_TOPICS(0.8), xbtlin/ai-berkshire: ALTERNATIVE(0.5), xorbitsai/inference: ALTERNATIVE(0.5), sierra-research/tau2-bench: ALTERNATIVE(0.5), langchain-ai/langchain: ALTERNATIVE(0.5), modelscope/ms-swift: ALTERNATIVE(0.5)]
ai_generated: false
human_edited: true
category: tool
rating: 5
maintenance: active
ai_tags: [llm, quant, multi-market, ai-agent, stock-analysis]
summary: |-
  LLM 多市场股票分析系统（6 万 star，MIT，活跃）：A股/港股/美股多源行情 + 实时新闻 + 决策看板 + 自动推送，GitHub Actions 零成本定时运行，被大量 fork 自用。
  
  **对你（trade-pulse 量化主线）的定位：架构升级的具体蓝图。** 两个核心借鉴点：① data_provider/ 抽象模式——把数据层解耦成 Provider 接口（摆脱对单一数据源的依赖）；② strategies/ 的 YAML 声明式信号设计。与 Vibe-Trading、Kronos、OpenBB、ai-berkshire 组成量化工具链。
---

# daily_stock_analysis

LLM 驱动的多市场股票智能分析系统：多源行情、实时新闻、决策看板与自动推送，支持零成本定时运行。  LLM-powered multi-market stock analysis system with multi-source market data, real-time news, decision dashboard, automated notifications, and cost-free scheduled runs.


## ✦ 人工摘要

LLM 多市场股票分析系统（6 万 star，MIT，活跃）：A股/港股/美股多源行情 + 实时新闻 + 决策看板 + 自动推送，GitHub Actions 零成本定时运行，被大量 fork 自用。

**对你（trade-pulse 量化主线）的定位：架构升级的具体蓝图。** 两个核心借鉴点：① data_provider/ 抽象模式——把数据层解耦成 Provider 接口（摆脱对单一数据源的依赖）；② strategies/ 的 YAML 声明式信号设计。与 Vibe-Trading、Kronos、OpenBB、ai-berkshire 组成量化工具链。


## TODO

### P2 — 参考其架构设计
- [ ] 参考 data_provider/ 抽象模式，改造 trade-pulse fetch_data.py 为 Provider 接口（先解耦 AkShare）
- [ ] 考虑将规则信号改为 YAML 声明式（参考 strategies/ 目录的设计）


## 评估

**分类**: tool
**评分**: 5/5
**维护状态**: active
**标签**: llm, quant, multi-market, ai-agent, stock-analysis
