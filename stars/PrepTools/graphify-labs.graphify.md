---
repo: Graphify-Labs/graphify
status: reviewed
language: Python
topics: [ai-agents, antigravity, ast, claude-code, code-analysis, code-search, codex, cursor, developer-tools, gemini, graphrag, knowledge-graph, leiden, llm, mcp, openclaw, rag, skills, tree-sitter]
relations: [Panniantong/Agent-Reach: SIMILAR_TOPICS(1.0), 1jehuang/jcode: SIMILAR_TOPICS(0.8), Canner/WrenAI: SIMILAR_TOPICS(0.8), Canner/WrenAI: ALTERNATIVE(0.5), AstrBotDevs/AstrBot: SIMILAR_TOPICS(1.0), AstrBotDevs/AstrBot: ALTERNATIVE(0.5), KnockOutEZ/wigolo: SIMILAR_TOPICS(1.0), tirth8205/code-review-graph: SIMILAR_TOPICS(1.0), tirth8205/code-review-graph: ALTERNATIVE(0.5), bojieli/ai-agent-book: SIMILAR_TOPICS(1.0), bojieli/ai-agent-book: ALTERNATIVE(0.5), affaan-m/ECC: SIMILAR_TOPICS(1.0), NevaMind-AI/memU: SIMILAR_TOPICS(1.0), Shubhamsaboo/awesome-llm-apps: ALTERNATIVE(0.5), OpenBB-finance/OpenBB: ALTERNATIVE(0.5), iOfficeAI/OfficeCLI: SIMILAR_TOPICS(1.0), addyosmani/agent-skills: SIMILAR_TOPICS(1.0), MadsLorentzen/ai-job-search: SIMILAR_TOPICS(0.8), CoplayDev/unity-mcp: SIMILAR_TOPICS(1.0), harvard-edge/cs249r_book: ALTERNATIVE(0.5), JuliusBrussee/caveman: SIMILAR_TOPICS(0.8), roboflow/supervision: ALTERNATIVE(0.5), diegosouzapw/OmniRoute: SIMILAR_TOPICS(1.0), HKUDS/Vibe-Trading: SIMILAR_TOPICS(0.8), HKUDS/Vibe-Trading: ALTERNATIVE(0.5), DeusData/codebase-memory-mcp: SIMILAR_TOPICS(1.0), alibaba/page-agent: SIMILAR_TOPICS(0.8), xbtlin/ai-berkshire: SIMILAR_TOPICS(1.0), xbtlin/ai-berkshire: ALTERNATIVE(0.5), ZhuLinsen/daily_stock_analysis: ALTERNATIVE(0.5), xorbitsai/inference: ALTERNATIVE(0.5), sierra-research/tau2-bench: ALTERNATIVE(0.5), langchain-ai/langchain: SIMILAR_TOPICS(1.0), langchain-ai/langchain: ALTERNATIVE(0.5), milvus-io/milvus: SIMILAR_TOPICS(0.8), modelscope/ms-swift: ALTERNATIVE(0.5), langgenius/dify: SIMILAR_TOPICS(1.0)]
ai_generated: false
human_edited: true
category: tool
rating: 5
maintenance: active
ai_tags: [knowledge-graph, code-analysis, ast, tree-sitter, developer-tools]
toolboxes: [agent-learning]
summary: |-
  代码知识图谱 skill（10 万 star，Apache 2.0，活跃）：本地 tree-sitter AST 确定性解析，把代码库+文档/SQL/PDF 转成可查询图谱，每条边可解释、无向量库。OpenClaw 生态相关（topics 含 openclaw）。
  
  **对你（代码理解）的定位：代码知识图谱三件套之一**（与 GitNexus、codebase-memory-mcp 重叠）。独特点：确定性解析 + 边可解释 + 无向量库，token 消耗小。建议实测后三选一：留 1 个主力 + 1 个备选，避免库膨胀。
---

# graphify

Turn any codebase, with its docs, SQL schemas, configs, and PDFs, into a queryable knowledge graph. A /graphify skill for Claude Code, Cursor, Codex, and Gemini CLI: local deterministic AST parsing, every edge explained, no vector store.


## ✦ 人工摘要

代码知识图谱 skill（10 万 star，Apache 2.0，活跃）：本地 tree-sitter AST 确定性解析，把代码库+文档/SQL/PDF 转成可查询图谱，每条边可解释、无向量库。OpenClaw 生态相关（topics 含 openclaw）。

**对你（代码理解）的定位：代码知识图谱三件套之一**（与 GitNexus、codebase-memory-mcp 重叠）。独特点：确定性解析 + 边可解释 + 无向量库，token 消耗小。建议实测后三选一：留 1 个主力 + 1 个备选，避免库膨胀。


## TODO


- [ ] 装进 OpenClaw 实测，与 GitNexus/codebase-memory-mcp 对比，确定代码图谱主力 (P2)

- [ ] 三选一后删除冗余项，保持库精简 (P2)




## 评估

**分类**: tool
**评分**: 5/5
**维护状态**: active
**标签**: knowledge-graph, code-analysis, ast, tree-sitter, developer-tools
