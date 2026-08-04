---
repo: shiyu-coder/Kronos
status: reviewed
language: Python
topics: [financial-market, foundation-model, deep-learning, transformer, time-series]
relations: []
ai_generated: false
human_edited: true
category: tool
rating: 5
maintenance: active
ai_tags: [financial-market, foundation-model, deep-learning, transformer, time-series]
toolboxes: [trade-pulse]
summary: |-
  首个开源金融 K 线基础模型（3.5 万 star，MIT，活跃，AAAI 2026）：45+ 全球交易所数据训练，专用 tokenizer + 自回归 Transformer 建模 K 线序列。
  
  **对你（trade-pulse 量化主线）：辅助方向模型，已验证推进中。** 作为与规则信号交叉验证的辅助模型——方向预测接入 daily_pipeline 当辅助信号。与 Vibe-Trading（回测/执行）、OpenBB（数据层）组成量化工具链。
---

# Kronos

Kronos: A Foundation Model for the Language of Financial Markets


## ✦ 人工摘要

首个开源金融 K 线基础模型（3.5 万 star，MIT，活跃，AAAI 2026）：45+ 全球交易所数据训练，专用 tokenizer + 自回归 Transformer 建模 K 线序列。

**对你（trade-pulse 量化主线）：辅助方向模型，已验证推进中。** 作为与规则信号交叉验证的辅助模型——方向预测接入 daily_pipeline 当辅助信号。与 Vibe-Trading（回测/执行）、OpenBB（数据层）组成量化工具链。


## TODO

### P1 — 立即可行
- [x] pip install + 下载 Kronos-mini 模型（4.1M 参数）
- [x] 喂 588000 历史日线，跑一次预测看效果
- [x] 对比 Kronos 预测方向 vs 规则信号的方向一致性

### P2 — 深度集成
- [ ] 将 Kronos direction score 接入 daily_pipeline 作为辅助信号
- [ ] 实盘稳定后，考虑用 588000 数据 fine-tune


## 评估

**分类**: tool
**评分**: 5/5
**维护状态**: active
**标签**: financial-market, foundation-model, deep-learning, transformer, time-series
