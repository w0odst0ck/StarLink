---
repo: artidoro/qlora
status: reviewed
language: Jupyter Notebook
topics: [quantization, finetuning, llm, lora]
relations: []
ai_generated: false
human_edited: true
category: tutorial
rating: 3
maintenance: active
ai_tags: [quantization, finetuning, llm, lora, nlp]
toolboxes: [ms-swift]
summary: |-
  QLoRA 论文（2023）的官方实现——用 4-bit 量化（NF4）+ 低秩适配（LoRA）+ 双重量化 + 分页优化器，把微调显存需求砍到可在一张 48GB 卡上微调 65B 模型。1.1 万 star，MIT。
  
  **对你（微调学习路线）的价值：** **论文必读，代码不用跑**。NF4 量化、双重量化、分页优化器是微调领域的基础原理，面试/工程里绕不开；但原始仓库是研究原型（Jupyter），实际微调请直接用现代框架——你库里的 ms-swift、或 Unsloth/HF PEFT 都已内置 QLoRA。你的 RTX 3060 12GB 上微调 7B 级模型，走 ms-swift 即可。
---

# qlora

QLoRA: Efficient Finetuning of Quantized LLMs


## ✦ 人工摘要

QLoRA 论文（2023）的官方实现——用 4-bit 量化（NF4）+ 低秩适配（LoRA）+ 双重量化 + 分页优化器，把微调显存需求砍到可在一张 48GB 卡上微调 65B 模型。1.1 万 star，MIT。

**对你（微调学习路线）的价值：** **论文必读，代码不用跑**。NF4 量化、双重量化、分页优化器是微调领域的基础原理，面试/工程里绕不开；但原始仓库是研究原型（Jupyter），实际微调请直接用现代框架——你库里的 ms-swift、或 Unsloth/HF PEFT 都已内置 QLoRA。你的 RTX 3060 12GB 上微调 7B 级模型，走 ms-swift 即可。


## TODO


- [ ] 读 QLoRA 论文（arXiv 2305.14314），吃透 NF4 量化 / 双重量化 / 分页优化器三个核心点 (P2)

- [ ] 对比 ms-swift 里 QLoRA 的实现与原始论文的差异（默认参数、量化位宽） (P3)

- [ ] 实操：用 ms-swift 在 RTX 3060 上微调一个小模型（7B 级），验证 QLoRA 显存收益 (P3)




## 评估

**分类**: tutorial
**评分**: 3/5
**维护状态**: active
**标签**: quantization, finetuning, llm, lora, nlp
