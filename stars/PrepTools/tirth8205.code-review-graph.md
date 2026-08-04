---
repo: tirth8205/code-review-graph
status: reviewed
language: Python
topics: [ai-coding, claude, claude-code, code-review, graphrag, incremental, knowledge-graph, llm, mcp, python, static-analysis, tree-sitter]
relations: [Panniantong/Agent-Reach: SIMILAR_TOPICS(1.0), 1jehuang/jcode: SIMILAR_TOPICS(1.0), Canner/WrenAI: ALTERNATIVE(0.5), AstrBotDevs/AstrBot: SIMILAR_TOPICS(1.0), AstrBotDevs/AstrBot: ALTERNATIVE(0.5), KnockOutEZ/wigolo: SIMILAR_TOPICS(0.8), bojieli/ai-agent-book: SIMILAR_TOPICS(0.8), bojieli/ai-agent-book: ALTERNATIVE(0.5), affaan-m/ECC: SIMILAR_TOPICS(1.0), Graphify-Labs/graphify: SIMILAR_TOPICS(1.0), Graphify-Labs/graphify: ALTERNATIVE(0.5), Shubhamsaboo/awesome-llm-apps: ALTERNATIVE(0.5), OpenBB-finance/OpenBB: ALTERNATIVE(0.5), CoplayDev/unity-mcp: SIMILAR_TOPICS(1.0), harvard-edge/cs249r_book: ALTERNATIVE(0.5), JuliusBrussee/caveman: SIMILAR_TOPICS(1.0), roboflow/supervision: ALTERNATIVE(0.5), diegosouzapw/OmniRoute: SIMILAR_TOPICS(1.0), HKUDS/Vibe-Trading: SIMILAR_TOPICS(1.0), HKUDS/Vibe-Trading: ALTERNATIVE(0.5), DeusData/codebase-memory-mcp: SIMILAR_TOPICS(1.0), xbtlin/ai-berkshire: SIMILAR_TOPICS(1.0), xbtlin/ai-berkshire: ALTERNATIVE(0.5), ZhuLinsen/daily_stock_analysis: ALTERNATIVE(0.5), calesthio/OpenMontage: SIMILAR_TOPICS(0.8), xorbitsai/inference: ALTERNATIVE(0.5), sierra-research/tau2-bench: ALTERNATIVE(0.5), langchain-ai/langchain: SIMILAR_TOPICS(0.8), langchain-ai/langchain: ALTERNATIVE(0.5), modelscope/ms-swift: ALTERNATIVE(0.5), langgenius/dify: SIMILAR_TOPICS(1.0)]
ai_generated: false
human_edited: true
category: tool
rating: 4
maintenance: active
ai_tags: [python, tree-sitter, mcp, static-analysis, knowledge-graph]
toolboxes: [starlink-self]
summary: |-
  本地代码智能图谱（2.8 万 star，MIT，活跃）：tree-sitter 建持久代码图，让 AI 审查只读相关上下文，token 降 38x-528x，MCP + CLI 支持。
  
  **对你（ocr review 工作流）的定位：代码审查场景的知识图谱。** 与 GitNexus/codebase-memory-mcp/graphify 区分：这个是**审查专用**——大仓库审查时只喂相关上下文，直接省 DeepSeek token 成本。可接入现有「提交前 ocr review」流程。
---

# code-review-graph

Local-first code intelligence graph for MCP and CLI. Builds a persistent map of your codebase so AI coding tools read only what matters, with benchmarked context reductions on reviews and large-repo workflows.


## ✦ 人工摘要

本地代码智能图谱（2.8 万 star，MIT，活跃）：tree-sitter 建持久代码图，让 AI 审查只读相关上下文，token 降 38x-528x，MCP + CLI 支持。

**对你（ocr review 工作流）的定位：代码审查场景的知识图谱。** 与 GitNexus/codebase-memory-mcp/graphify 区分：这个是**审查专用**——大仓库审查时只喂相关上下文，直接省 DeepSeek token 成本。可接入现有「提交前 ocr review」流程。


## TODO


- [ ] 接进 ocr review 工作流：审查前先建图谱，实测 token 节省与审查质量 (P2)

- [ ] 与 graphify/codebase-memory-mcp 对比，确定审查场景的主力方案 (P3)




## 评估

**分类**: tool
**评分**: 4/5
**维护状态**: active
**标签**: python, tree-sitter, mcp, static-analysis, knowledge-graph
