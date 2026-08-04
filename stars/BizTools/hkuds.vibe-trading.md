---
repo: HKUDS/Vibe-Trading
status: reviewed
language: Python
topics: [ai-agent, algorithmic-trading, backtesting, fintech, llm, mcp, multi-agent, python, quantitative-finance, trading]
relations: [Panniantong/Agent-Reach: SIMILAR_TOPICS(1.0), 1jehuang/jcode: SIMILAR_TOPICS(1.0), Canner/WrenAI: ALTERNATIVE(0.5), AstrBotDevs/AstrBot: SIMILAR_TOPICS(1.0), AstrBotDevs/AstrBot: ALTERNATIVE(0.5), KnockOutEZ/wigolo: SIMILAR_TOPICS(0.8), tirth8205/code-review-graph: SIMILAR_TOPICS(1.0), tirth8205/code-review-graph: ALTERNATIVE(0.5), bojieli/ai-agent-book: SIMILAR_TOPICS(1.0), bojieli/ai-agent-book: ALTERNATIVE(0.5), affaan-m/ECC: SIMILAR_TOPICS(0.8), Graphify-Labs/graphify: SIMILAR_TOPICS(0.8), Graphify-Labs/graphify: ALTERNATIVE(0.5), Shubhamsaboo/awesome-llm-apps: ALTERNATIVE(0.5), OpenBB-finance/OpenBB: SIMILAR_TOPICS(0.8), OpenBB-finance/OpenBB: ALTERNATIVE(0.5), CoplayDev/unity-mcp: SIMILAR_TOPICS(0.8), harvard-edge/cs249r_book: ALTERNATIVE(0.5), roboflow/supervision: ALTERNATIVE(0.5), xbtlin/ai-berkshire: SIMILAR_TOPICS(1.0), xbtlin/ai-berkshire: ALTERNATIVE(0.5), ZhuLinsen/daily_stock_analysis: SIMILAR_TOPICS(1.0), ZhuLinsen/daily_stock_analysis: ALTERNATIVE(0.5), xorbitsai/inference: ALTERNATIVE(0.5), sierra-research/tau2-bench: ALTERNATIVE(0.5), langchain-ai/langchain: SIMILAR_TOPICS(0.8), langchain-ai/langchain: ALTERNATIVE(0.5), modelscope/ms-swift: ALTERNATIVE(0.5), langgenius/dify: SIMILAR_TOPICS(1.0)]
ai_generated: false
human_edited: true
category: tool
rating: 5
maintenance: active
ai_tags: [ai-agent, algorithmic-trading, backtesting, llm, quantitative-finance]
toolboxes: [trade-pulse]
summary: |-
  港大 HKUDS 的 LLM 多智能体交易系统（2.9 万 star，MIT，活跃）：AI Agent + 多智能体协作做算法交易、回测，支持 MCP/API 接口，一键安装。
  
  **对你（trade-pulse 量化主线）的定位：交易回测与执行层的候选引擎。** 已规划三阶段接入：P1 适配器（加载日线信号 JSON → 触发回测）→ P2 回测验证（588000 对比自测结果）→ P3 执行层（vn.py 连接东财 + Shadow Account 模拟盘 → 真实资金）。与 shiyu-coder/Kronos、xbtlin/ai-berkshire、ZhuLinsen/daily_stock_analysis 同为量化工具链成员。
---

# Vibe-Trading

"Vibe-Trading: Your Personal Trading Agent"


## ✦ 人工摘要

港大 HKUDS 的 LLM 多智能体交易系统（2.9 万 star，MIT，活跃）：AI Agent + 多智能体协作做算法交易、回测，支持 MCP/API 接口，一键安装。

**对你（trade-pulse 量化主线）的定位：交易回测与执行层的候选引擎。** 已规划三阶段接入：P1 适配器（加载日线信号 JSON → 触发回测）→ P2 回测验证（588000 对比自测结果）→ P3 执行层（vn.py 连接东财 + Shadow Account 模拟盘 → 真实资金）。与 shiyu-coder/Kronos、xbtlin/ai-berkshire、ZhuLinsen/daily_stock_analysis 同为量化工具链成员。


## TODO

### P1 — 评估适配器可行性
- [ ] pip install vibe-trading-ai，跑 quick start demo
- [ ] 读 Vibe-Trading Strategy / Backtest API 文档，确认接口签名
- [ ] 写最小 adapter：加载日线信号 JSON → 触发回测

### P2 — 回测验证
- [ ] 用 Vibe-Trading 引擎回测 588000，对比 trade-pulse 自测结果
- [ ] 确认绩效指标一致（作为适配器 sanity check）

### P3 — Shadow Account + 执行层
- [ ] 配置 vn.py 连接器，确认能否绑定东方财富账户
- [ ] 开 Shadow Account 模拟盘，观察执行稳定性
- [ ] 稳定后切换真实资金


## 评估

**分类**: tool
**评分**: 5/5
**维护状态**: active
**标签**: ai-agent, algorithmic-trading, backtesting, llm, quantitative-finance
