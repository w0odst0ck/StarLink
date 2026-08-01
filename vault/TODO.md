# StarLink TODO
共 218 项

## 1jehuang/jcode
- [ ] 有空装来跑一次，对比与 OpenClaw 的内存占用和交互体验 (P3)
- [ ] 了解其 MCP 集成方式，作为 agent 工具设计参考 (P3)

## AstrBotDevs/AstrBot
- [ ] 看其国内 IM（QQ/飞书）接入实现，对比自己的飞书 webhook 链路方案 (P3)
- [ ] 了解其插件市场机制，与 OpenClaw skills 体系对照 (P3)

## ByteByteGoHq/system-design-101
- [ ] 独立站架构设计时，按需查阅对应章节（API 设计/数据库选型/缓存/CDN） (P3)
- [ ] 面试准备阶段，系统过一遍核心章节 (P3)

## Canner/WrenAI
- [ ] 跑通 quickstart，体验自然语言→SQL→图表全流程，记录生成质量 (P3)
- [ ] 与 Chat2DB 对比：text-to-SQL 准确率、语义层设计、部署成本，沉淀选型结论 (P3)
- [ ] 独立站数据分析场景预研：把经营数据接进去，验证"非技术用户问数据"的可行性 (P3)

## ChromeDevTools/chrome-devtools-mcp
- [ ] 接进 OpenClaw：配置 chrome-devtools-mcp，实测控制真实 Chrome 完成一次自动化操作 (P2)
- [ ] 评估爬虫调试场景：JS 渲染页面、反爬对抗时的断点/网络/性能检查能力 (P2)
- [ ] 与 puppeteer 直连方式对比，明确什么场景用 MCP 更省事 (P3)

## CoplayDev/unity-mcp
- [ ] 启动 3D 内容/仿真可视化方向时，评估 AI 控制 Unity 的自动化生产流程 (P3)
- [ ] 了解其 47 个工具的能力边界（资源/场景/脚本），作为 MCP 设计参考 (P3)

## DeusData/codebase-memory-mcp
- [ ] 装进 OpenClaw，拿学习项目（如 pi）索引，实测结构查询效果 (P2)
- [ ] 与 GitNexus 对比选型：性能/集成/使用体验，确定代码智能主力工具 (P2)

## Evil0ctal/Douyin_TikTok_Download_API
- [ ] 接进信息采集管线：抖音/B站数据采集，作为舆情/热点信源 (P2)
- [ ] 了解其反爬机制（签名算法/无水印），沉淀逆向经验 (P3)
- [ ] 与 MediaCrawler 对比选型：API 下载 vs 全量爬取，按场景分工 (P3)

## Graphify-Labs/graphify
- [ ] 装进 OpenClaw 实测，与 GitNexus/codebase-memory-mcp 对比，确定代码图谱主力 (P2)
- [ ] 三选一后删除冗余项，保持库精简 (P2)

## HKUDS/Vibe-Trading
- [ ] pip install vibe-trading-ai，跑 quick start demo (P3)
- [ ] 读 Vibe-Trading Strategy / Backtest API 文档，确认接口签名 (P3)
- [ ] 写最小 adapter：加载日线信号 JSON → 触发回测 (P3)
- [ ] 用 Vibe-Trading 引擎回测 588000，对比 trade-pulse 自测结果 (P3)
- [ ] 确认绩效指标一致（作为适配器 sanity check） (P3)
- [ ] 配置 vn.py 连接器，确认能否绑定东方财富账户 (P3)
- [ ] 开 Shadow Account 模拟盘，观察执行稳定性 (P3)
- [ ] 稳定后切换真实资金 (P3)

## IceWhaleTech/CasaOS
- [ ] 有自托管/家用服务硬件时再评估，当前不投入 (P3)

## JuliusBrussee/caveman
- [ ] 跟进其更新（新强度分级/压缩技巧），评估是否调优自己的模式配置 (P3)
- [ ] 对比 OmniRoute 的 RTK+Caveman 压缩实现，看有无可借鉴点 (P3)

## KnockOutEZ/wigolo
- [ ] 试接进 OpenClaw，对比与自带 web_search 的搜索/抓取效果差异 (P3)
- [ ] 评估其 crawl/scrape 能力在爬虫管线中的补充价值 (P3)

## MadsLorentzen/ai-job-search
- [ ] 有求职/跳槽需求时启用：fork 填个人 profile，跑 /setup → /scrape → /apply 流程 (P3)
- [ ] 作为 agent 工作流范式参考：学它如何编排「评估→定制→生成」多步流程 (P3)

## NanmiCoder/MediaCrawler
- [ ] 接进信息采集管线：小红书/微博/B站内容采集，作为舆情/热点信源 (P2)
- [ ] 与 Douyin_TikTok_Download_API 分工：全平台采集 vs 视频下载，按场景选用 (P3)
- [ ] 明确合规边界（数据使用范围），避免法律风险 (P2)

## NevaMind-AI/memU
- [ ] 读其 500 行核心逻辑，理解「记忆 → 技能提炼」的实现机制 (P2)
- [ ] 评估借鉴点：能否把自动技能提炼的思路引入自己的记忆沉淀流程（MEMORY.md 维护自动化） (P3)
- [ ] 了解跨 Agent 记忆共享方案，对比 OpenClaw 子 session 的记忆隔离设计 (P3)

## OpenBB-finance/OpenBB
- [ ] 评估接入 trade-pulse：对比 OpenBB 与现有数据源（akshare 类）的覆盖/稳定性，确定数据层方案 (P2)
- [ ] MCP Server 接进 OpenClaw，实测 AI 查询金融数据（588000 行情/宏观指标） (P2)
- [ ] 与 Vibe-Trading 适配器联动：OpenBB 提供数据 → Vibe-Trading 回测 (P3)

## OtterMind/Chat2DB
- [ ] trade-pulse 数据量级上来后，用它做日常查询/分析 (P3)
- [ ] 与 WrenAI 一起对比选型：客户端 GUI vs 服务端 BI，按场景分工 (P3)

## Panniantong/Agent-Reach
- [ ] 维护 cookie 配置（平台风控变化时及时更新），保证采集链路可用 (P2)
- [ ] 量化舆情管线接入：国内信源（B站/小红书）并入 trade-pulse 情绪因子 (P2)
- [ ] 独立站热点捕获：用它对国内内容平台做趋势监测 (P2)

## PostHog/posthog
- [ ] 独立站上线前评估部署（Docker 自托管，注意 Postgres+ClickHouse 依赖），设计埋点方案 (P3)
- [ ] 上线后接入：事件追踪 + 转化漏斗分析，配合 CRO 优化（与 marketingskills 联动） (P3)
- [ ] 了解功能开关/A-B 实验能力，为独立站迭代实验做准备 (P3)

## Robbyant/lingbot-map
- [ ] 自动驾驶仿真/3D 视觉方向启动时，研究其流式重建管线 (P3)

## Shubhamsaboo/awesome-llm-apps
- [ ] 做 RAG/Agent 项目前先检索对应模板（study-vault 检索、客服 Agent、分析 Agent） (P3)
- [ ] 把用得上的模板沉淀进自己的项目参考/代码库 (P3)

## THU-MAIC/OpenMAIC
- [ ] 浏览 live demo（open.maic.chat）感受多智能体课堂交互形态 (P3)
- [ ] 拆解其 LangGraph 多智能体编排结构，看角色分工与状态流转 (P2)
- [ ] 读 JCST 2026 论文，了解多智能体教学的设计动机与效果评估 (P3)
- [ ] 若需要自建，用 Vercel 一键部署 + 自己的 LLM key 试跑 (P3)

## Zackriya-Solutions/meetily
- [ ] 自用跟进即可 (P3)

## ZhuLinsen/daily_stock_analysis
- [ ] 参考 data_provider/ 抽象模式，改造 trade-pulse fetch_data.py 为 Provider 接口（先解耦 AkShare） (P3)
- [ ] 考虑将规则信号改为 YAML 声明式（参考 strategies/ 目录的设计） (P3)

## abhigyanpatwari/GitNexus
- [ ] 拿一个学习中的项目（如 pi）跑一次知识图谱，体验代码探索效率 (P2)
- [ ] 评估 MCP 接进 OpenClaw：AI 读代码时获取架构上下文的效果 (P2)

## addyosmani/agent-skills
- [ ] 读 2-3 个代表性 skill（如 code review / spec 类），拆解其结构设计（触发条件、步骤、输出约定） (P2)
- [ ] 借鉴其质量门禁思路，优化自己的「提交前 ocr review」流程设计 (P2)
- [ ] 评估哪些 skill 可以直接移植到 OpenClaw 用（注意平台差异） (P3)

## affaan-m/ECC
- [ ] 拆解其体系框架（skills/instincts/memory/security 如何组织），与 addyosmani/agent-skills 对比异同 (P3)
- [ ] 提取可借鉴的设计思想（如记忆组织、安全边界）到自己的 OpenClaw skill 体系 (P3)
- [ ] 持续观察 star 变化与社区反馈，判断是真价值还是营销泡沫 (P3)

## alibaba/open-code-review
- [ ] 梳理内置规则集覆盖的检查项（NPE/线程安全/XSS/SQL 注入等），对照自己项目的常见 bug 类型 (P2)
- [ ] 记录 ocr review 在真实项目上的漏报/误报案例，沉淀自己的审查补充清单 (P2)
- [ ] 评估提示词/规则定制空间，看能否把 trade-pulse 等项目的专属检查项加进去 (P3)

## alibaba/page-agent
- [ ] 拿一个复杂交互页面（多步骤表单/动态加载）试玩，评估它相对传统爬虫的适用边界 (P3)
- [ ] 看 MCP Server 集成方式，评估能否接进 OpenClaw 工具链 (P3)
- [ ] 独立站产品页加 AI 助手时，把它作为候选方案之一 (P3)

## alibaba/zvec
- [ ] 与 milvus/pymilvus 做本地 benchmark：小规模（<100 万向量）下的建索引速度、查询延迟、内存占用 (P2)
- [ ] 用 Python 绑定把 study-vault 类本地知识库接进 zvec 做语义检索 demo (P2)
- [ ] 看 v0.6.0 的 group-by search 与随机旋转量化特性，评估对召回率的提升 (P3)

## andrewyng/aisuite
- [ ] 信息采集/舆情管线里试接入：DeepSeek 为主 + 备选模型切换，验证统一接口效率 (P2)
- [ ] 看其 Agents API（工具/MCP），与 pi 的 agent 设计对照 (P3)

## artidoro/qlora
- [ ] 读 QLoRA 论文（arXiv 2305.14314），吃透 NF4 量化 / 双重量化 / 分页优化器三个核心点 (P2)
- [ ] 对比 ms-swift 里 QLoRA 的实现与原始论文的差异（默认参数、量化位宽） (P3)
- [ ] 实操：用 ms-swift 在 RTX 3060 上微调一个小模型（7B 级），验证 QLoRA 显存收益 (P3)

## bojieli/ai-agent-book
- [ ] 纳入学习路线排期：按章读 + 跑配套实验（Agent 原理/工具调用/多 Agent 协作） (P2)
- [ ] 重点章节：MCP、RAG、context engineering——与 OpenClaw 实际用法对照印证 (P2)
- [ ] 读书心得/实验总结沉淀进 study-vault 知识库 (P2)

## browser-use/video-use
- [ ] 启动 AI 短剧项目时，先评估它作为视频处理引擎的适用性（agent 驱动 ffmpeg 的工作流） (P3)
- [ ] 了解其能力边界：字幕/剪辑/特效覆盖度，对照短剧生产的实际需求 (P3)

## calesthio/OpenMontage
- [ ] 持续跟进版本更新与新管线，评估哪些能改进现有短剧工作流 (P2)
- [ ] 把基于 OpenMontage 的实践经验沉淀成自己的技能文件（对应它的 700+ skill 体系） (P2)
- [ ] 评估 AGPL 协议对商业化的约束，提前规划合规路径 (P3)

## chatwoot/chatwoot
- [ ] 独立站启动客服时，Docker 部署 Chatwoot 试运行，评估全渠道收件箱是否满足需求 (P3)
- [ ] 评估 Captain AI Agent 能力，与自己的 AI 客服方案（结合 τ-Bench 评测思路）对比 (P3)
- [ ] 看 API/webhook，评估与独立站订单系统对接的可行性 (P3)

## codecrafters-io/build-your-own-x
- [ ] 学习路线排到数据库/网络/编译器等内容时，配套做对应 "build your own X" 实践 (P2)
- [ ] 收藏几个最相关的教程（数据库、网络协议）备用 (P3)

## commaai/openpilot
- [ ] 研究其架构分层：Python 模型层 / C++ 控制层的边界与通信，提炼嵌入式 AI 改造范式 (P3)
- [ ] 了解其数据采集→训练→部署闭环，作为自动驾驶仿真方向的方法论参考 (P3)
- [ ] 启动嵌入式方向时，对照它的硬件选型与实时性设计 (P3)

## coreyhaines31/marketingskills
- [ ] 独立站上线后，选 2-3 个核心 skill（SEO/文案/CRO）移植到 OpenClaw 用起来 (P2)
- [ ] 学其 skill 结构设计（触发、步骤、输出），对照优化自己的 skill 写法 (P3)
- [ ] 评估哪些营销场景可以 agent 化：竞品分析、关键词研究、落地页文案生成 (P3)

## deepseek-ai/awesome-deepseek-integration
- [ ] 新项目需要 DeepSeek 集成时，查对应现成方案 (P3)

## diegosouzapw/OmniRoute
- [ ] 个人开发场景：了解其 token 压缩与免费池机制，评估能否降低 OpenClaw 日常 API 成本 (P3)
- [ ] 独立站 AI 功能做高可用时：对比 OmniRoute vs 自建 LiteLLM 网关的可靠性/合规/可控性 (P3)
- [ ] 明确隐私边界：客户数据是否允许经过第三方网关，写入独立站技术决策记录 (P3)

## different-ai/openwork
- [ ] 了解其工作流共享机制（如何跨 agent 复用 skills/MCP），对比自己的 skill 移植需求 (P3)
- [ ] 多工具协作或团队场景出现时，评估是否引入 (P3)

## dontbesilent2025/dbskill
- [ ] 拆解其「知识原子 → skill」的组织结构，对照优化自己的 skill 体系 (P3)
- [ ] 评估其商业诊断框架能否用于独立站业务分析（定位/产品/增长） (P3)

## earendil-works/pi
- [ ] 从 pi 源码学 agent 核心：agent loop（循环）、工具调用协议、上下文管理 (P1)
- [ ] 用 pi 搭一个自己的最小 agent demo（接 DeepSeek API，带 1-2 个工具） (P1)
- [ ] 对照 LangGraph 的 agent 设计，整理两种生态的异同（状态管理/工具协议） (P2)
- [ ] 尝试用 pi 实现一个实际场景（如独立站客服 agent 原型） (P2)

## fastapi/fastapi
- [ ] 给爬虫管线搭一个 FastAPI 服务层：数据查询 API + 定时任务状态接口 (P2)
- [ ] 量化信号推送：把 trade-pulse 的每日信号包成 FastAPI 接口，供飞书/前端消费 (P2)
- [ ] 掌握关键模式：依赖注入、Pydantic 模型校验、async + 连接池（异步 DB/Redis） (P2)

## geo-tp/ESP32-Bit-Pirate
- [ ] 嵌入式方向启动时，入手 ESP32 + 刷 Bit Pirate 固件，熟悉协议调试 (P2)
- [ ] 用它系统过一遍常见协议（I2C/SPI/UART/CAN），作为嵌入式学习实操环节 (P2)

## github/spec-kit
- [ ] 在下一个项目（trade-pulse 新功能 / 独立站模块）试用 SDD 流程：先写 spec → plan → tasks，再开发 (P2)
- [ ] 评估适配方案：specify CLI 生成文档 + OpenClaw 读文档执行，记录适配成本 (P3)
- [ ] 学其流程设计（constitution/specify/plan/tasks 拆分粒度），沉淀自己的 AI 开发流程规范 (P3)

## harvard-edge/cs249r_book
- [ ] 纳入学习路线：ML 系统章节排期（训练/推理/部署工程实践） (P2)
- [ ] 跑 TinyTorch 实验，从零实现一个最小训练框架 (P2)
- [ ] 重点读嵌入式/边缘 ML 章节，对接嵌入式智能化改造方向 (P2)

## hasaneyldrm/exercises-dataset
- [ ] 需要时用它的 JSON 数据做训练计划/动作库查询小工具（本地或脚本级） (P3)
- [ ] 了解数据 schema（肌肉群/器械/动作步骤字段），看能否覆盖自己的训练记录需求 (P3)

## hugohe3/ppt-master
- [ ] 用真实周报数据试跑一次：把周报要点 + 项目数据转成带图表的汇报 PPT (P2)
- [ ] 摸清自定义模板能力，固化一套自己汇报风格的模板 (P2)
- [ ] 了解图表/表格从数据自动生成的方式，沉淀数据→PPT 的工作流 (P3)

## iOfficeAI/OfficeCLI
- [ ] 接进 OpenClaw 试跑：让 AI 读/改一份周报 Word 文档，验证「渲染-查看-修改」闭环 (P2)
- [ ] 与 ppt-master 配合，走通「数据表格 → 周报文档 + 汇报 PPT」的自动化流程 (P2)
- [ ] 摸清 Excel 数据处理能力（读表/改表/公式），用于数据整理场景 (P3)

## ibelick/ui-skills
- [ ] 独立站 UI 改版/美化时，评估其技能包能否提升 AI 生成界面质量 (P3)

## jamiepine/voicebox
- [ ] AI 短剧项目启动时，评估其配音工作流（声音克隆 + TTS）能否满足生产需求 (P3)
- [ ] 3060 上实测声音克隆质量与生成速度，对比 ElevenLabs 效果 (P3)

## kvcache-ai/ktransformers
- [ ] 本地 3060 实测：部署 ktransformers 跑一个 MoE 模型（如 DeepSeek 系），对比 ollama 的吞吐与显存占用 (P2)
- [ ] 看官方教程里的 CPU-GPU 专家调度原理，理解异构推理的取舍（首 token 延迟 vs 吞吐） (P2)
- [ ] 联动 ms-swift：微调后的模型用 ktransformers 部署，走通"微调→部署"闭环 (P3)

## langchain-ai/langchain
- [ ] 用 LangGraph 把 trade-pulse 信号流程改造成 agent：拉数据→算因子→出信号→发提醒，状态机化 (P2)
- [ ] 吃透核心概念：StateGraph 节点/边/条件路由、checkpoint 持久化、human-in-the-loop 打断恢复 (P2)
- [ ] 对比 LangGraph 与 OpenClaw/autogen 的编排模型差异，沉淀选型心得 (P3)

## langgenius/dify
- [ ] 自部署一次 Dify，用 study-vault 知识库搭一个 RAG 工作流 demo，体验交付效率 (P3)
- [ ] 与 LangGraph 做选型对比：同一个小需求（如信号分析问答）分别实现，记录开发耗时与定制自由度 (P3)
- [ ] 关注 MCP 插件生态，评估 Dify 接入外部工具链的能力边界 (P3)

## lyogavin/airllm
- [ ] 在 3060 上跑一次 AirLLM（选一个小模型验证链路），实测吞吐，与 ktransformers 对比 (P3)
- [ ] 明确适用场景：离线批量推理（如批量文档摘要）可接受慢，实时交互不可用 (P3)
- [ ] 了解其分层推理原理（layer-by-layer 加载），与量化方案（GPTQ/AWQ）的取舍对比 (P3)

## mattpocock/skills
- [ ] 读 2-3 个代表性 skill，拆解其结构（输入/步骤/输出约定），借鉴到自己的 OpenClaw skills (P2)
- [ ] 评估哪些可直接移植（模型无关特性） (P3)

## microsoft/PowerToys
- [ ] 自用跟进，无需额外研究 (P3)

## microsoft/generative-ai-for-beginners
- [ ] 快速过一遍核心概念课：提示工程、RAG、LLM 原理，对照自己的实践查漏补缺 (P3)
- [ ] 需要时把课程里的概念图/框架沉淀进 study-vault 知识库 (P3)

## milvus-io/milvus
- [ ] 规划独立站向量检索选型路线图：起步 pgvector/zvec → 量级上来迁移 milvus，记录迁移路径 (P2)
- [ ] Docker 起 milvus standalone + pymilvus 走通 CRUD 和搜索，熟悉基础用法 (P3)
- [ ] 对比 milvus 与 zvec 在同一数据集上的查询延迟/吞吐/运维成本，作为未来选型依据 (P3)

## milvus-io/pymilvus
- [ ] 用 milvus 时安装对应版本 SDK，先查版本兼容表再升级 (P3)
- [ ] 跟着 milvus 实操走一遍 quickstart：连接、建 collection、插入、搜索 (P3)

## modelscope/ms-swift
- [ ] 3060 上走通完整微调流程：pip install ms-swift → 选 7B 级模型（Qwen3 系）→ LoRA/QLoRA 微调 → 推理验证 (P1)
- [ ] 实测 LoRA vs QLoRA 在 3060 上的显存占用与效果差异，记录数据 (P2)
- [ ] 微调产物导出，用 ktransformers/ollama 部署，走通「微调→部署」闭环 (P2)
- [ ] 进阶：了解 GRPO/DPO 对齐训练入口，为后续对齐实验铺路 (P3)

## msitarzewski/agency-agents
- [ ] 拆解其 agent 定义结构（角色/流程/交付物），与 ECC 体系对比异同 (P3)
- [ ] 提取可借鉴的角色化设计思想到自己的 OpenClaw skills (P3)

## mvanhorn/last30days-skill
- [ ] 装进 OpenClaw，用真实主题（如某标的舆情）跑一次完整调研，评估输出质量 (P1)
- [ ] 配置 Reddit/X/YouTube 等平台 API key，打通多信源 (P1)
- [ ] 量化方向：把舆情简报接入 trade-pulse 信号管线，作为情绪因子（结合 Kronos 验证） (P2)
- [ ] 独立站方向：用它做竞品/趋势热点捕获，沉淀选题流程 (P2)

## obra/superpowers
- [ ] 关注其方法论更新，看是否有值得补充进自己 skill 的新设计 (P3)

## ollama/ollama
- [ ] 3060 上装好 ollama + 拉一个 7B 级模型（Qwen3 系），确认 GPU 加速生效（nvidia-smi 观察显存占用） (P1)
- [ ] 用 REST API（/api/generate、/api/chat）从 FastAPI 脚本调本地模型，走通「本地模型服务化」 (P2)
- [ ] 同一模型对比 ollama 与 ktransformers 的吞吐/显存，记录数据 (P3)

## openclaw/openclaw
- [ ] 跟进新版本能力（工具/skills 生态/渠道），评估升级价值 (P2)
- [ ] 持续维护自身配置与 skills 体系（memory 归档、技能沉淀） (P2)
- [ ] 关注 VISION.md 路线图，提前了解未来方向 (P3)

## opendatalab/MinerU
- [ ] 接入 study-vault 入库流程：PDF 资料转 markdown 再入库，验证效果 (P2)
- [ ] 实测复杂 PDF（扫描件/公式/表格）的 OCR 与版面还原质量 (P2)
- [ ] 信息采集管线里处理 PDF 报告类信源时优先用它 (P3)

## paperswithbacktest/awesome-systematic-trading
- [ ] 按需检索：回测库/数据源/策略实现，选型时先查它的清单 (P2)
- [ ] 把发现的优质资源（书/库/博客）沉淀进 study-vault 量化域 (P3)

## pbakaus/impeccable
- [ ] 独立站 UI 改版时，配 ui-skills 一起用：AI 生成 → impeccable 质检迭代 (P3)
- [ ] 学其确定性规则设计（60 条检测器），借鉴到自己的审查类 skill (P3)

## punkpeye/awesome-mcp-servers
- [ ] 给 OpenClaw 找扩展能力/新工具时，先检索此清单 (P3)
- [ ] agent 开发（pi）需要现成 server 时查阅 (P3)

## refactoringhq/tolaria
- [ ] 需要本地可视化浏览/编辑 Markdown 知识库时，评估 tolaria 是否优于现有链路 (P3)

## ripienaar/free-for-dev
- [ ] 独立站上线前，用它的清单选免费基建方案（DB/CDN/邮件/监控） (P3)
- [ ] 新项目需要免费服务/额度时按需检索 (P3)

## roboflow/supervision
- [ ] 视觉方向启动时，配 cs249r_book CV 章节做检测/跟踪实践 (P2)
- [ ] 嵌入式摄像头方案结合 supervision 做目标检测原型 (P3)

## ruvnet/RuView
- [ ] 嵌入式方向启动时，研究其 ESP32 固件 + CSI 采集/处理管线 (P3)
- [ ] 了解其边缘 AI 栈（RuVector/Cognitum），评估感知层方案选型 (P3)

## shiyu-coder/Kronos
- [x] pip install + 下载 Kronos-mini 模型（4.1M 参数） (P3)
- [x] 喂 588000 历史日线，跑一次预测看效果 (P3)
- [x] 对比 Kronos 预测方向 vs 规则信号的方向一致性 (P3)
- [ ] 将 Kronos direction score 接入 daily_pipeline 作为辅助信号 (P3)
- [ ] 实盘稳定后，考虑用 588000 数据 fine-tune (P3)

## sierra-research/tau2-bench
- [ ] 了解其评测维度：工具调用正确率、任务成功率、成本权衡，理解 Agent 评测方法论 (P3)
- [ ] 做独立站 AI 客服时，参考 τ-Bench 场景设计自己的客服评测集（模拟对话 + 工具调用） (P3)
- [ ] 用 LangGraph 搭的 agent 跑一遍 τ-Bench 小样本，熟悉评测流程 (P3)

## simplex-chat/simplex-chat
- [ ] 自用跟进即可，无需额外研究 (P3)

## tirth8205/code-review-graph
- [ ] 接进 ocr review 工作流：审查前先建图谱，实测 token 节省与审查质量 (P2)
- [ ] 与 graphify/codebase-memory-mcp 对比，确定审查场景的主力方案 (P3)

## virgiliojr94/book-to-skill
- [ ] 拿学习路线中的一本技术书试转换，评估生成的 skill 质量（框架/决策规则提取） (P2)
- [ ] 评估适配 OpenClaw：生成的 skill 直接可用 or 需要转换 (P2)
- [ ] 与 study-vault 知识入库流程结合，形成「书→知识→技能」完整链路 (P3)

## vxcontrol/pentagi
- [ ] 独立站上线前做安全评估时，评估用它做自动化渗透测试 (P3)
- [ ] 研究其多 Agent 编排 + 沙箱隔离架构，作技术参考 (P3)

## wistbean/learn_python3_spider
- [ ] 按需查：遇到反爬/逆向场景时检索对应章节（CSS 加密、JS 逆向、验证码） (P3)
- [ ] 复习抓包链路：fiddler/mitmproxy 手机 APP 抓包流程，跟上 MediaCrawler 等实战项目配合用 (P3)
- [ ] 把常用脚本整理成自己的小工具箱（代理池、验证码、去重存储） (P3)

## xbtlin/ai-berkshire
- [ ] 在 trade-pulse 决策门中实现对抗验证：规则信号 vs Kronos 预测方向一致才执行 (P3)
- [ ] 信号冲突时设计暂缓/降仓规则（参考 ai-berkshire 的裁判 Agent 模式） (P3)

## xorbitsai/inference
- [ ] 明确切换场景：多模态/语音推理、生产级 API 部署时才用 Xinference，日常用 ollama (P3)
- [ ] 对比 ollama 与 Xinference 的 API 兼容性、模型支持面、部署复杂度，记一份选型备忘 (P3)
- [ ] 若独立站需要统一模型 API 层，评估 Xinference 做模型网关的可行性 (P3)

## zilliztech/attu
- [ ] 用 milvus 时配 attu 做可视化管理，无需单独研究 (P3)
