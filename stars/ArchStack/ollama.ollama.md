---
repo: ollama/ollama
status: reviewed
language: Go
topics: [deepseek, gemma, gemma3, glm, go, golang, gpt-oss, llama, llama3, llm, llms, minimax, mistral, ollama, qwen]
relations: [lyogavin/airllm: SIMILAR_TOPICS(0.8), AstrBotDevs/AstrBot: SIMILAR_TOPICS(0.8), Zackriya-Solutions/meetily: SIMILAR_TOPICS(0.8), diegosouzapw/OmniRoute: SIMILAR_TOPICS(0.8), xorbitsai/inference: SIMILAR_TOPICS(1.0), milvus-io/milvus: SIMILAR_TOPICS(0.8), milvus-io/milvus: ALTERNATIVE(0.5), modelscope/ms-swift: SIMILAR_TOPICS(0.8)]
ai_generated: false
human_edited: true
category: tool
rating: 5
maintenance: active
ai_tags: [llm, local-ai, go, open-source, model-serving]
toolboxes: [ms-swift]
summary: |-
  本地运行 LLM 的傻瓜式工具（17.7 万 star，MIT，今日仍活跃）。`ollama run <model>` 一条命令拉模型跑起来，自带 CLI + REST API，支持 Qwen/DeepSeek/GLM/Kimi 等主流模型。
  
  **对你（3060 本地 AI）的定位：日常开发默认入口——"docker for models"。** 实验、开发、联调用它零配置起步。完整链路：**微调用 ms-swift，日常跑用 ollama，极限性能/大模型上 ktransformers**。REST API 是 FastAPI 对接本地模型的桥梁。
---

# ollama

Get up and running with Kimi-K2.6, GLM-5.2, MiniMax, DeepSeek, gpt-oss, Qwen, Gemma and other models.


## ✦ 人工摘要

本地运行 LLM 的傻瓜式工具（17.7 万 star，MIT，今日仍活跃）。`ollama run <model>` 一条命令拉模型跑起来，自带 CLI + REST API，支持 Qwen/DeepSeek/GLM/Kimi 等主流模型。

**对你（3060 本地 AI）的定位：日常开发默认入口——"docker for models"。** 实验、开发、联调用它零配置起步。完整链路：**微调用 ms-swift，日常跑用 ollama，极限性能/大模型上 ktransformers**。REST API 是 FastAPI 对接本地模型的桥梁。


## TODO


- [ ] 3060 上装好 ollama + 拉一个 7B 级模型（Qwen3 系），确认 GPU 加速生效（nvidia-smi 观察显存占用） (P1)

- [ ] 用 REST API（/api/generate、/api/chat）从 FastAPI 脚本调本地模型，走通「本地模型服务化」 (P2)

- [ ] 同一模型对比 ollama 与 ktransformers 的吞吐/显存，记录数据 (P3)




## 评估

**分类**: tool
**评分**: 5/5
**维护状态**: active
**标签**: llm, local-ai, go, open-source, model-serving
