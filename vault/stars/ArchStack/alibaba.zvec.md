---
repo: alibaba/zvec
status: reviewed
language: C++
topics: [agent-skills, db, embedded, faiss, hnsw, llm-memory, local, rag, search-engine, semantic-search, similarity-search, vector-database, vector-db]
relations: [KnockOutEZ/wigolo: SIMILAR_TOPICS(0.8), milvus-io/pymilvus: SIMILAR_TOPICS(0.8), milvus-io/milvus: SIMILAR_TOPICS(1.0)]
ai_generated: false
human_edited: true
category: lib
rating: 4
maintenance: active
ai_tags: [vector-database, similarity-search, embedded, rag, cpp]
toolboxes: [indiestore]
summary: |-
  阿里开源的嵌入式（in-process）向量数据库，C++ 实现，主打轻量 + 极速。支持稠密/稀疏向量、全文检索、混合查询，可直接嵌进应用进程（类似 SQLite 的定位），提供 Python/Node.js 绑定。1.5 万 star，Apache 2.0，活跃维护。
  
  **对你（RAG 选型）的价值：** 与库里的 milvus/pymilvus 形成互补——milvus 是分布式重型服务，zvec 是嵌入式轻量款。本地小规模 RAG / LLM 记忆 / 个人知识库语义检索场景，用 zvec 免运维、零部署成本；量级上来再上 milvus。做 study-vault 类本地知识库语义检索时，优先试它。
---

# zvec

A lightweight, lightning-fast, in-process vector database


## ✦ 人工摘要

阿里开源的嵌入式（in-process）向量数据库，C++ 实现，主打轻量 + 极速。支持稠密/稀疏向量、全文检索、混合查询，可直接嵌进应用进程（类似 SQLite 的定位），提供 Python/Node.js 绑定。1.5 万 star，Apache 2.0，活跃维护。

**对你（RAG 选型）的价值：** 与库里的 milvus/pymilvus 形成互补——milvus 是分布式重型服务，zvec 是嵌入式轻量款。本地小规模 RAG / LLM 记忆 / 个人知识库语义检索场景，用 zvec 免运维、零部署成本；量级上来再上 milvus。做 study-vault 类本地知识库语义检索时，优先试它。


## TODO


- [ ] 与 milvus/pymilvus 做本地 benchmark：小规模（<100 万向量）下的建索引速度、查询延迟、内存占用 (P2)

- [ ] 用 Python 绑定把 study-vault 类本地知识库接进 zvec 做语义检索 demo (P2)

- [ ] 看 v0.6.0 的 group-by search 与随机旋转量化特性，评估对召回率的提升 (P3)




## 评估

**分类**: lib
**评分**: 4/5
**维护状态**: active
**标签**: vector-database, similarity-search, embedded, rag, cpp
