---
repo: xorbitsai/inference
status: reviewed
language: Python
topics: [artificial-intelligence, chatglm, deployment, flan-t5, gemma, ggml, glm4, inference, llama, llama3, llamacpp, llm, machine-learning, mistral, openai-api, pytorch, qwen, vllm, whisper, wizardlm]
relations: [microsoft/AI-For-Beginners: SIMILAR_TOPICS(0.8), Canner/WrenAI: ALTERNATIVE(0.5), lyogavin/airllm: SIMILAR_TOPICS(0.8), AstrBotDevs/AstrBot: SIMILAR_TOPICS(0.8), AstrBotDevs/AstrBot: ALTERNATIVE(0.5), tirth8205/code-review-graph: ALTERNATIVE(0.5), bojieli/ai-agent-book: ALTERNATIVE(0.5), Graphify-Labs/graphify: ALTERNATIVE(0.5), Shubhamsaboo/awesome-llm-apps: ALTERNATIVE(0.5), OpenBB-finance/OpenBB: ALTERNATIVE(0.5), harvard-edge/cs249r_book: SIMILAR_TOPICS(0.8), harvard-edge/cs249r_book: ALTERNATIVE(0.5), Zackriya-Solutions/meetily: SIMILAR_TOPICS(0.8), roboflow/supervision: SIMILAR_TOPICS(0.8), roboflow/supervision: ALTERNATIVE(0.5), HKUDS/Vibe-Trading: ALTERNATIVE(0.5), xbtlin/ai-berkshire: ALTERNATIVE(0.5), ZhuLinsen/daily_stock_analysis: ALTERNATIVE(0.5), sierra-research/tau2-bench: ALTERNATIVE(0.5), ollama/ollama: SIMILAR_TOPICS(1.0), langchain-ai/langchain: ALTERNATIVE(0.5), modelscope/ms-swift: SIMILAR_TOPICS(0.8), modelscope/ms-swift: ALTERNATIVE(0.5)]
ai_generated: false
human_edited: true
category: lib
rating: 4
maintenance: active
ai_tags: [llm-inference, openai-api, multimodal, python]
toolboxes: [ms-swift]
summary: |-
  Xinference——统一推理引擎（9.5k star，Apache 2.0，活跃）。LLM/语音/多模态模型统一成 OpenAI 兼容 API 部署，支持 vLLM 后端、自动批处理、云端/本地，主打"改一行代码换模型"。
  
  **对你（本地推理）的定位：ollama 的工程化备选。** 日常快速跑用 ollama（更傻瓜、生态更大）；需要多模态/语音/生产级部署时切 Xinference。两者功能重叠，不必都深度研究——主用 ollama，按需切换。
---

# inference

Swap GPT for any LLM by changing a single line of code. Xinference lets you run open-source, speech, and multimodal models on cloud, on-prem, or your laptop — all through one unified, production-ready inference API.


## ✦ 人工摘要

Xinference——统一推理引擎（9.5k star，Apache 2.0，活跃）。LLM/语音/多模态模型统一成 OpenAI 兼容 API 部署，支持 vLLM 后端、自动批处理、云端/本地，主打"改一行代码换模型"。

**对你（本地推理）的定位：ollama 的工程化备选。** 日常快速跑用 ollama（更傻瓜、生态更大）；需要多模态/语音/生产级部署时切 Xinference。两者功能重叠，不必都深度研究——主用 ollama，按需切换。


## TODO


- [ ] 明确切换场景：多模态/语音推理、生产级 API 部署时才用 Xinference，日常用 ollama (P3)

- [ ] 对比 ollama 与 Xinference 的 API 兼容性、模型支持面、部署复杂度，记一份选型备忘 (P3)

- [ ] 若独立站需要统一模型 API 层，评估 Xinference 做模型网关的可行性 (P3)




## 评估

**分类**: lib
**评分**: 4/5
**维护状态**: active
**标签**: llm-inference, openai-api, multimodal, python
