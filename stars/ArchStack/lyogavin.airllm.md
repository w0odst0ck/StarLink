---
repo: lyogavin/airllm
status: reviewed
language: Python
topics: [chinese-llm, chinese-nlp, finetune, generative-ai, instruct-gpt, instruction-set, llama, llm, lora, open-models, open-source, open-source-models, qlora]
relations: [microsoft/AI-For-Beginners: ALTERNATIVE(0.5), AstrBotDevs/AstrBot: SIMILAR_TOPICS(0.8), xorbitsai/inference: SIMILAR_TOPICS(0.8), ollama/ollama: SIMILAR_TOPICS(0.8), langchain-ai/langchain: SIMILAR_TOPICS(1.0), modelscope/ms-swift: SIMILAR_TOPICS(1.0)]
ai_generated: false
human_edited: true
category: tool
rating: 4
maintenance: active
ai_tags: [llm, inference, gpu-optimization, memory-efficient, deep-learning]
toolboxes: [ms-swift]
summary: |-
  AirLLM——极低显存跑超大模型的推理方案（2.4 万 star，Apache 2.0，活跃）。原理是分层推理：逐层把权重加载进显存计算，不量化不蒸馏，4GB 可跑 70B、12GB 可跑 DeepSeek-V3 671B。
  
  **对你（3060 12GB）的价值：兜底方案，不是主力。** 代价是速度极慢——逐层反复加载权重，吞吐远低于正常推理，只适合离线/批量/实验场景。与 ktransformers（异构调度、需内存配合、快）形成互补：**要快 → KTransformers，没内存只能等 → AirLLM**。
---

# airllm

AirLLM 70B inference with single 4GB GPU


## ✦ 人工摘要

AirLLM——极低显存跑超大模型的推理方案（2.4 万 star，Apache 2.0，活跃）。原理是分层推理：逐层把权重加载进显存计算，不量化不蒸馏，4GB 可跑 70B、12GB 可跑 DeepSeek-V3 671B。

**对你（3060 12GB）的价值：兜底方案，不是主力。** 代价是速度极慢——逐层反复加载权重，吞吐远低于正常推理，只适合离线/批量/实验场景。与 ktransformers（异构调度、需内存配合、快）形成互补：**要快 → KTransformers，没内存只能等 → AirLLM**。


## TODO


- [ ] 在 3060 上跑一次 AirLLM（选一个小模型验证链路），实测吞吐，与 ktransformers 对比 (P3)

- [ ] 明确适用场景：离线批量推理（如批量文档摘要）可接受慢，实时交互不可用 (P3)

- [ ] 了解其分层推理原理（layer-by-layer 加载），与量化方案（GPTQ/AWQ）的取舍对比 (P3)




## 评估

**分类**: tool
**评分**: 4/5
**维护状态**: active
**标签**: llm, inference, gpu-optimization, memory-efficient, deep-learning
