---
repo: kvcache-ai/ktransformers
status: reviewed
language: Python
topics: [llm, inference, fine-tuning, cpu-gpu, heterogeneous-computing]
relations: []
ai_generated: false
human_edited: true
category: framework
rating: 5
maintenance: active
ai_tags: [llm, inference, heterogeneous-computing, cpu-gpu, moe]
toolboxes: [ms-swift]
summary: |-
  清华 kvcache.ai 团队的开源异构 LLM 推理/微调框架（1.9 万 star，Apache 2.0，活跃）。核心思路：MoE 模型的专家层调度到 CPU 内存，GPU 只跑关键计算，让消费级显卡跑起远超显存的大模型。
  
  **对你（RTX 3060 12GB）的价值：这是你本地跑大模型的最优解之一**——12GB 显存 + 内存异构，可跑 70B 级 MoE 模型，配合 LLaMA-Factory/SGLang 生态。与 ollama（傻瓜部署）、ms-swift（微调）互补：想要吞吐和极限性能就上它。
---

# ktransformers

A Flexible Framework for Experiencing Heterogeneous LLM Inference/Fine-tune Optimizations


## ✦ 人工摘要

清华 kvcache.ai 团队的开源异构 LLM 推理/微调框架（1.9 万 star，Apache 2.0，活跃）。核心思路：MoE 模型的专家层调度到 CPU 内存，GPU 只跑关键计算，让消费级显卡跑起远超显存的大模型。

**对你（RTX 3060 12GB）的价值：这是你本地跑大模型的最优解之一**——12GB 显存 + 内存异构，可跑 70B 级 MoE 模型，配合 LLaMA-Factory/SGLang 生态。与 ollama（傻瓜部署）、ms-swift（微调）互补：想要吞吐和极限性能就上它。


## TODO


- [ ] 本地 3060 实测：部署 ktransformers 跑一个 MoE 模型（如 DeepSeek 系），对比 ollama 的吞吐与显存占用 (P2)

- [ ] 看官方教程里的 CPU-GPU 专家调度原理，理解异构推理的取舍（首 token 延迟 vs 吞吐） (P2)

- [ ] 联动 ms-swift：微调后的模型用 ktransformers 部署，走通"微调→部署"闭环 (P3)




## 评估

**分类**: framework
**评分**: 5/5
**维护状态**: active
**标签**: llm, inference, heterogeneous-computing, cpu-gpu, moe
