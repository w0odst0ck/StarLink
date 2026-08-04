---
repo: modelscope/ms-swift
status: reviewed
language: Python
topics: [deepseek-r1, embedding, grpo, internvl, liger, llama, llama4, llm, lora, megatron, moe, multimodal, open-r1, peft, qwen3, qwen3-6, qwen3-omni, qwen3-vl, reranker, sft]
relations: [Canner/WrenAI: ALTERNATIVE(0.5), lyogavin/airllm: SIMILAR_TOPICS(1.0), AstrBotDevs/AstrBot: SIMILAR_TOPICS(0.8), AstrBotDevs/AstrBot: ALTERNATIVE(0.5), tirth8205/code-review-graph: ALTERNATIVE(0.5), bojieli/ai-agent-book: SIMILAR_TOPICS(0.8), bojieli/ai-agent-book: ALTERNATIVE(0.5), Graphify-Labs/graphify: ALTERNATIVE(0.5), Shubhamsaboo/awesome-llm-apps: ALTERNATIVE(0.5), OpenBB-finance/OpenBB: ALTERNATIVE(0.5), harvard-edge/cs249r_book: ALTERNATIVE(0.5), roboflow/supervision: ALTERNATIVE(0.5), HKUDS/Vibe-Trading: ALTERNATIVE(0.5), xbtlin/ai-berkshire: ALTERNATIVE(0.5), ZhuLinsen/daily_stock_analysis: ALTERNATIVE(0.5), xorbitsai/inference: SIMILAR_TOPICS(0.8), xorbitsai/inference: ALTERNATIVE(0.5), sierra-research/tau2-bench: ALTERNATIVE(0.5), ollama/ollama: SIMILAR_TOPICS(0.8), langchain-ai/langchain: ALTERNATIVE(0.5)]
ai_generated: false
human_edited: true
category: framework
rating: 5
maintenance: active
ai_tags: [llm, multimodal, fine-tuning, peft, megatron]
toolboxes: [ms-swift]
summary: |-
  阿里魔搭的微调/部署一体化框架（1.5 万 star，Apache 2.0，AAAI 2025）。600+ LLM、300+ 多模态模型，支持 PEFT/全参/DPO/GRPO，训练→推理→量化一条龙，中文文档、国产模型生态（Qwen/DeepSeek/GLM）友好。
  
  **对你（微调学习路线）的定位：微调实操第一工具。** 分工明确：qlora 仓库学原理（NF4/双重量化），ms-swift 动手干——你的 RTX 3060 12GB 上微调 7B 级模型（QLoRA/LoRA）就用它，一条命令走通。是 W1 学习路径模型训练环节的执行主力。
---

# ms-swift

Use PEFT or Full-parameter to CPT/SFT/DPO/GRPO 600+ LLMs (Qwen3.6, DeepSeek-V4, GLM-5.1, InternLM3, Llama4, ...) and 300+ MLLMs (Qwen3-VL, Qwen3-Omni, InternVL3.5, Ovis2.5, GLM4.5v, Gemma4, Llava, Phi4, ...) (AAAI 2025).


## ✦ 人工摘要

阿里魔搭的微调/部署一体化框架（1.5 万 star，Apache 2.0，AAAI 2025）。600+ LLM、300+ 多模态模型，支持 PEFT/全参/DPO/GRPO，训练→推理→量化一条龙，中文文档、国产模型生态（Qwen/DeepSeek/GLM）友好。

**对你（微调学习路线）的定位：微调实操第一工具。** 分工明确：qlora 仓库学原理（NF4/双重量化），ms-swift 动手干——你的 RTX 3060 12GB 上微调 7B 级模型（QLoRA/LoRA）就用它，一条命令走通。是 W1 学习路径模型训练环节的执行主力。


## TODO


- [ ] 3060 上走通完整微调流程：pip install ms-swift → 选 7B 级模型（Qwen3 系）→ LoRA/QLoRA 微调 → 推理验证 (P1)

- [ ] 实测 LoRA vs QLoRA 在 3060 上的显存占用与效果差异，记录数据 (P2)

- [ ] 微调产物导出，用 ktransformers/ollama 部署，走通「微调→部署」闭环 (P2)

- [ ] 进阶：了解 GRPO/DPO 对齐训练入口，为后续对齐实验铺路 (P3)




## 评估

**分类**: framework
**评分**: 5/5
**维护状态**: active
**标签**: llm, multimodal, fine-tuning, peft, megatron
