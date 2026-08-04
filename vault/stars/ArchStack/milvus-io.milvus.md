---
repo: milvus-io/milvus
status: reviewed
language: Go
topics: [anns, cloud-native, diskann, distributed, embedding-database, embedding-similarity, embedding-store, faiss, golang, hnsw, image-search, llm, nearest-neighbor-search, rag, vector-database, vector-search, vector-similarity, vector-store]
relations: [Canner/WrenAI: SIMILAR_TOPICS(0.8), bojieli/ai-agent-book: SIMILAR_TOPICS(0.8), Graphify-Labs/graphify: SIMILAR_TOPICS(0.8), alibaba/zvec: SIMILAR_TOPICS(1.0), ollama/ollama: SIMILAR_TOPICS(0.8), ollama/ollama: ALTERNATIVE(0.5), milvus-io/pymilvus: SIMILAR_TOPICS(1.0), langchain-ai/langchain: SIMILAR_TOPICS(0.8), langgenius/dify: SIMILAR_TOPICS(0.8)]
ai_generated: false
human_edited: true
category: tool
rating: 5
maintenance: active
ai_tags: [vector-database, approximate-nearest-neighbor-search, cloud-native, distributed, golang]
summary: |-
  云原生分布式向量数据库标杆（4.5 万 star，Apache 2.0，活跃）。支持 ANN 搜索、混合查询、实时更新、水平扩展，是生产级 RAG/多模态检索的行业标准。
  
  **对你（独立站 AI 商业产品）的定位：第二阶段的基础设施，起步不用它。** 独立站 AI 客服/商品语义搜索起步阶段（<10 万向量），用 zvec 或 pgvector 轻量方案即可；数据量上来（十万级+、高并发、多租户 SaaS）再迁移 milvus——生态成熟（pymilvus SDK + LangChain/Dify 集成），迁移成本可控。
---

# milvus

Milvus is a high-performance, cloud-native vector database built for scalable vector ANN search


## ✦ 人工摘要

云原生分布式向量数据库标杆（4.5 万 star，Apache 2.0，活跃）。支持 ANN 搜索、混合查询、实时更新、水平扩展，是生产级 RAG/多模态检索的行业标准。

**对你（独立站 AI 商业产品）的定位：第二阶段的基础设施，起步不用它。** 独立站 AI 客服/商品语义搜索起步阶段（<10 万向量），用 zvec 或 pgvector 轻量方案即可；数据量上来（十万级+、高并发、多租户 SaaS）再迁移 milvus——生态成熟（pymilvus SDK + LangChain/Dify 集成），迁移成本可控。


## TODO


- [ ] 规划独立站向量检索选型路线图：起步 pgvector/zvec → 量级上来迁移 milvus，记录迁移路径 (P2)

- [ ] Docker 起 milvus standalone + pymilvus 走通 CRUD 和搜索，熟悉基础用法 (P3)

- [ ] 对比 milvus 与 zvec 在同一数据集上的查询延迟/吞吐/运维成本，作为未来选型依据 (P3)




## 评估

**分类**: tool
**评分**: 5/5
**维护状态**: active
**标签**: vector-database, approximate-nearest-neighbor-search, cloud-native, distributed, golang
