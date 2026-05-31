# AI Project Context Map

> 用途：给未来的通用 AI 大模型、开发者、审查者快速理解本文件夹。  
> 当前盘点时间：2026-05-31。  
> 路径约定：本文不绑定具体电脑路径；统一使用 `<母交付包根目录>` 表示本文件所在目录。

## 0. 总体判断

这个根目录不是单一仓库，而是一个多项目交付包集合。核心脉络是：

```text
Q-SpecTrum 智脑平台
  ├─ Ghost Channel / 幽灵通道：多智能体通讯与记忆同步协议
  ├─ QCM-MVP-Emergence：共鸣公式、22 公式、涌现验证
  ├─ Universal-KB / 数据库管理应用：知识库、文件整理、MCP 工具层
  └─ AI项目管理知识库：角色、技能、平台 DB、长期记忆、协作流程
```

`<母交付包根目录>` 采用 **Git Monorepo** 结构管理：
- 根目录本身是一个 git 仓库（main 分支），负责母包级文档和 `00.超级提示词工程` 的版本控制。
- `03.数据库管理_文件夹整理AI应用` 和 `05.超极智脑_Q-SpecTrum` 作为 git submodule 引入（03→knowledge-base-manager main, 05→Q-Spectrum master）。
- fresh clone 后 submodule 默认可能显示 `HEAD (no branch)`；只读/验证可接受。若要修改 03/05，先在子模块目录内切到对应分支（03=`main`, 05=`master`），再 commit+push，最后回根目录更新 submodule 引用。

根目录还包含核心方法论技能文件 `qcm-universal-ai-system-v3.0.skill`（ZIP，45角色/9阶段/24维/5子代理），这是QCM质量评估框架的完整定义，AI在深度模式下按阶段激活角色子集。

根目录新增 `MISSION-MEMORY.md`，作为母交付包长期使命、身份边界、自然语言唤醒握手和记忆写入原则的第一入口。根目录 `MOTHER-PACK-ACTIVATION-GUIDE.md` 是**唯一的权威AI启动协议**，所有其他文档中的启动步骤均为其扩展或简化版本。未来 AI 进入母包时，应先读 `MISSION-MEMORY.md`，再读本文件。

## 0.1 交付包边界

本目录未来有两层交付含义：

```text
<母交付包根目录>/                         # 母交付包/开发者包：先压缩交付给开发者的完整生产系统
└── 协同通用AI大模型开发交付包/             # 用户交付包模板/最终装配区：开发者完成具体项目后交付给最终用户
```

规划原则：

- 不在文档、脚本、提示词中硬编码本机绝对路径。
- 母交付包面向开发者，保留源项目、研究资料、历史报告、开发仓库、SDK、提示词工程和验证体系。
- 用户交付包面向最终用户，不是母交付包的简单镜像；它应承载某个具体项目的价值体系、功能体系、结构体系、运作体系。
- 开发者先接收母交付包，再用母交付包开发具体项目，最后把 `协同通用AI大模型开发交付包/` 整理、验证、压缩后交给最终用户。
- 用户交付包应从母交付包中抽取必要能力，形成可迁移、可验证、可运行、可协作的项目成果包。

## 1. 顶层目录地图

| 目录 | 当前状态 | 定位 | 关键入口 |
|---|---:|---|---|
| `00.超级提示词工程` | 79 文件 | 跨项目 AI 协同的提示词操作系统与审计控制平面：总控启动、引导秘书、使命记忆唤醒、SpecForge、Skill Gate、源提示词吸收、全链路审计、机器可读注册表、统一状态对象、知识结晶、沙盘记录、首次对话冷启动、自举协同开发实例 | `README.md`, `01-总控提示词/MASTER-ORCHESTRATOR-PROMPT.md`, `12-引导秘书逻辑/GUIDE-SECRETARY-PROTOCOL.md`, `15-超级系统提示词工程/FIRST-DIALOG-BOOTSTRAP-PROMPT.md`, `15-超级系统提示词工程/FIRST-DIALOG-COLD-START-DECONSTRUCTION.md`, `14-全链路审计与运行对齐/SELF-BOOTSTRAP-PROJECT-SPEC-AND-RUN.md`, `14-全链路审计与运行对齐/SANDBOX-RUN-20260531-AI-COLLABORATION-COLD-START-SIMULATION.md`, `14-全链路审计与运行对齐/VALIDATION_REGISTRY.yaml`, `14-全链路审计与运行对齐/ATOMIC-FILE-INVENTORY-SUMMARY.md` |
| `01.通讯协议_幽灵通道` | 296 文件 | Ghost Channel v1.0 协议、SDK、部署与商业交付包 | `README.md`, `INDEX.md`, `00_总览/PROJECT_HANDOFF.md`, `VERIFY.ps1` |
| `02.通用知识库框架_Universal-KB` | 28 文件 | Universal-KB 通用知识库模板；完整可运行知识库应用以 03 为准 | `README.md`, `INDEX.md`, `04-memory/memoryos.py`, `05-agents/AGENTS.md` |
| `03.数据库管理_文件夹整理AI应用` | 153 文件 | V2 知识库应用：Flask + MCP + 文件整理 + 向量检索（子工作区） | `README.md`, `AGENTS.md`, `app.py`, `mcp_server.py`, `verify_install.py` |
| `04.QCM-MVP-Emergence` | 148 文件 | QCM 共鸣/涌现 MVP，22 公式实现、角色/沙盘/飞轮与运行入口 | `README.md`, `PROJECT_HANDOFF-QCM.md`, `qcm/main.py`, `health_check.py` |
| `05.超极智脑_Q-SpecTrum` | 423 文件 | 主平台：15 角色、Web UI、API、MCP、DB、知识库、验证门（子工作区） | `README.md`, `INDEX.md`, `AGENTS.md`, `智腦協議-BRAIN-PROTOCOL.md`, `run.py`, `api_server.py`, `qspectrum_mcp_server.py` |
| `协同通用AI大模型开发交付包` | 14 文件 | 开发者完成具体项目后交给最终用户的交付包骨架，承载价值/功能/结构/运作四体系，并提供普通/Strict 两种交付验证模式 | `README.md`, `AI_PROJECT_CONTEXT.md`, `HANDOFF.md`, `VALIDATION_REPORT.md`, `TRACEABILITY-MATRIX.md`, `VERIFY-DELIVERY.ps1` |

统计口径：以上采用 `00.超级提示词工程/14-全链路审计与运行对齐/ATOMIC-FILE-INVENTORY-SUMMARY.md` 当前审计口径，排除 `.git`、`__pycache__`、`.pytest_cache`、`node_modules`、`dist/build/coverage` 等运行缓存；当前全量展开为 1155 文件。

## 2. 子系统理解

### 2.1 `01.通讯协议_幽灵通道`

定位：Q-SpecTrum 的对外通讯协议层，目标是多智能体记忆同步、因果一致性、增量同步、完整性验证和企业部署。

三层 SDK：

```text
ghost_channel              # 开源协议核心，src layout
  -> ghost_channel_sdk      # 轻量 SDK，依赖 ghost-channel
  -> ghost_hub_sdk          # 企业 SDK，意图银行 + IoT 无 UI 适配 + Agent 联邦
```

关键能力：

- Delta 同步、Vector Clock、Merkle 完整性、AES/HMAC 加密、审计日志、自愈快照。
- `GhostHub_SDK/templates/` 含 23 个业务模板。
- `04_企业部署/` 含 Docker、K8s、授权、监控、商业部署内容。

验证注意：

- 当前已复跑 SDK 测试：开源核心 18 passed、轻量 SDK 68 passed、企业 SDK 76 passed、TypeScript SDK 22 passed，合计 184 passed。
- 当前 `GhostHub_SDK/pyproject.toml` 已修复早期报告提到的根包缺失问题，包含 `ghost_hub_sdk` 根包和 FastAPI/Pydantic/Uvicorn/MQTT/WebSocket 依赖。
- `VERIFY.ps1` 已修复自校验跳过正则，兼容 `MANIFEST.yaml :` 这种冒号前带空格的 manifest 行。
- 轻量 SDK 公开包名以 `ghost_channel_sdk` 为准；历史旧 import 示例已在 B2 收敛。

### 2.2 `02.通用知识库框架_Universal-KB`

定位：通用知识管理模板，不是完整运行应用。

核心链路：

```text
01-raw -> 02-processed -> 03-wiki -> 04-memory -> 05-agents -> 06-output
```

关键文件：

- `03-wiki/index.md`：知识图谱索引。
- `04-memory/memoryos.py`：三层记忆引擎。
- `05-agents/AGENTS.md`：Ingest / Query / Lint 行为配置。
- 当前 `04-memory/memoryos.py` 可编译并可运行 smoke test；smoke 使用临时目录，不再在母包根目录生成 `test_memory`。本目录仍应按“轻量模板”使用，不应等同于 `03` 的完整可运行应用。

### 2.3 `03.数据库管理_文件夹整理AI应用`

定位：Universal-KB V2 可运行应用，面向文件整理、知识沉淀、AI 协作和 MCP 工具调用。

运行入口：

```bash
python verify_install.py
python app.py --port 5000
python mcp_server.py
pytest tests -q
```

当前验证：

- `python verify_install.py`：23 通过、0 失败、1 警告。
- 警告仅为未配置 `.env`，影响 API key/高级 AI 调用，不影响基础运行。
- `pytest tests -q` 当前 107 passed。

核心模块：

- `app.py`：Flask Web/REST/CLI，端口默认 5000；提供搜索、浏览 wiki、ingest、memory、maintain、API index 等。
- `mcp_server.py`：MCP server，暴露 `search_all`、`vector_search`、`search_memory`、`process_file`、`project_decision_workflow` 等 20 个工具。
- `.workbuddy/scripts/`：搜索、向量、自动整理、收件箱、工作流、模型适配、项目关系分析等脚本。
- `.workbuddy/记忆层/`：MemoryOS、任务记忆、经验库、项目知识。
- `.workbuddy/index/search_index.db`：当前有 `documents` 表，约 23 条索引记录。

### 2.4 `04.QCM-MVP-Emergence`

定位：QCM 理论的可执行 MVP，验证“幽灵通道协议 + 共鸣公式 = 涌现发生”。

核心公式：

```text
R(e_i, e_j) = 0.35*K_sim + 0.40*C_comp + 0.25*I_freq
涌现阈值：R > 0.85
```

实现结构：

- `02-代码编写/`：公式、测试和演示入口。
- `qcm/`：命名空间包，包含 core、enhanced、evolution、decision、capabilities、roles、collaboration、sandbox、flywheel、summoning。
- `01-幽灵通道SDK/`：嵌入的 Ghost Channel SDK 副本。

当前验证：

- `python "02-代码编写/test_qcm_all.py"`：25 PASS / 0 FAIL。
- `pytest test_roles/test_collaboration/test_sandbox/test_flywheel/test_summoning -q`：38 passed。
- `python health_check.py`：6/6 checks passed，状态 `READY`。

### 2.5 `05.超极智脑_Q-SpecTrum`

定位：主平台，也是未来通用 AI 协作开发时最重要的根系统。它把角色、知识库、协议、Web UI、API、MCP、记忆、任务、反馈闭环串起来。

优先阅读顺序：

```text
INDEX.md
AGENTS.md
智腦協議-BRAIN-PROTOCOL.md
_HANDOFF/STATUS.md
_HANDOFF/CRITICAL-REMINDERS.md
_HANDOFF/MEMORY-INDEX.md
README.md
```

运行入口：

```bash
python verify-integration.py
$env:PYTHONUTF8='1'; python run.py --status
python run.py --web
python run.py --query "你的问题"
python scripts/security-check.py
```

当前验证：

- `python verify-integration.py`：PASS；`_HANDOFF/` 是 runtime handoff 提示，不是硬失败。
- `python run.py --status`：当前已做 UTF-8 输出硬化，显示 `System: ALL GREEN`。
- `pytest tests -q`：158 passed。
- `python run.py --e2e`：13 passed / 0 failed。
- API smoke：`/api/status`、`/api/roles`、`/api/chat` 路由 Q02/Q06/Q08 通过。
- MCP stdio smoke：18 tools，status resource、execute_chat、SELECT-only DB 查询通过，stdout 无非 JSON 污染。
- 平台数据库权威路径：`AI项目管理/Platform/db/platform.db`，当前 15 角色。

核心模块：

- `qspectrum_engine.py`：主引擎。`QSpectrumDB -> Secretary -> KnowledgeResonance -> PromptBuilder -> LLMProvider -> QSpectrumEngine.process()`。
- `api_server.py`：REST API + 静态 Web UI，默认端口 8765，包含 `/api/chat`、roles、knowledge、ghost-channel、closed-loop、projects、tasks、memory、files、scenarios、skills 等端点。
- `run.py`：CLI/Web/status/e2e/guide 统一入口。
- `brain_core/`：已抽出的可复用脑模块，包括 config、graph、MCP bridge、capabilities、brain、hybrid router、knowledge orchestrator、skill orchestrator 等。
- `BRAIN-KB/`：P0-P1 长期知识，包含 decisions、knowledge、limitations、patterns。
- `AI项目管理/Platform/db/platform.db` 是当前代码权威平台 DB；根目录 `platform.db` 不应作为主路径假设。

文档漂移：

- `requirements.txt` 与 `pyproject.toml` 当前均声明 `chromadb>=1.5.0`、`networkx>=3.0`；README / QUICK-START / INSTALL-GUIDE 已对齐为 Python 3.10+ 与 `pip install -r requirements.txt`。

## 3. 跨系统集成关系

```text
Ghost Channel
  提供通信/同步/审计/安全协议
  被 Q-SpecTrum 的 ghost_channel_adapter.py、ghost_channel_gate.py 概念性吸收
  也被 QCM-MVP 的 SDK 副本用于公式/协议演示

QCM-MVP-Emergence
  提供共鸣公式、角色协同、沙盘、飞轮、召唤、涌现检测
  其理论成果在 Q-SpecTrum 的 QCM、KnowledgeResonance、R formula 中体现

Universal-KB V1/V2
  提供知识沉淀目录范式、MemoryOS、文件整理、检索、MCP 工具
  `03` 是更可运行的应用版，`02` 是轻模板

Q-SpecTrum
  是集成层：角色系统 + 平台 DB + Web/API + MCP + 记忆 + 任务 + 反馈闭环
  未来开发优先围绕 `05` 展开，必要时引用 `01/03/04` 的成熟模块
```

## 4. 原子能力索引

| 能力族 | 原子能力 | 主要来源 |
|---|---|---|
| 通信协议 | Delta sync、VectorClock、Merkle、AES/HMAC、Audit、Snapshot | `01`, `04/01-幽灵通道SDK`, `05/ghost_channel_*` |
| 知识管理 | wiki、concept/entity/source/comparison、MemoryOS、search index | `02`, `03`, `05/BRAIN-KB` |
| 检索 | 关键词搜索、文件名搜索、FAISS/向量搜索、SQLite 查询 | `03/.workbuddy/scripts`, `05/global_search.py` |
| AI 协作 | 15 角色、Secretary 路由、协作协议、双轨审查 | `05`, `04/qcm/roles`, `04/qcm/collaboration` |
| 涌现公式 | R 公式、22 公式、动态权重、飞轮、沙盘、神经路由、Pareto | `04`, `05/qspectrum_engine.py` |
| 执行接口 | Flask Web、MCP stdio、REST API、CLI、Web chat UI | `03/app.py`, `03/mcp_server.py`, `05/run.py`, `05/api_server.py` |
| 质量验证 | install verify、QCM tests、integration verify、security checks、audit suites | `03/tests`, `04/tests`, `05/tests`, `01/VERIFY.ps1` |
| 部署商业 | Docker、K8s、license server、monitoring、pricing/sales docs | `01/04_企业部署`, `01/05_商业化与市场` |

## 5. 建议的未来 AI 协作流程

> **权威启动协议**: 标准AI唤醒序列以根目录 `MOTHER-PACK-ACTIVATION-GUIDE.md` 的"AI 激活序列"章节为准。普通聊天框冷启动先使用 `00.超级提示词工程/15-超级系统提示词工程/FIRST-DIALOG-BOOTSTRAP-PROMPT.md`。以下为扩展参考。

每次新模型进入根目录，先读 `MOTHER-PACK-ACTIVATION-GUIDE.md` 完成标准唤醒激活，再按任务进入子系统。若任务涉及交付链路，必须先判断是在维护母交付包，还是在组装某个具体项目的用户交付包：

1. 冷启动模式判断：若无 System Prompt 输入框，发送 `00.超级提示词工程/15-超级系统提示词工程/FIRST-DIALOG-BOOTSTRAP-PROMPT.md` 的首条消息。
2. 使命唤醒：读 `MISSION-MEMORY.md`，确认母包使命、模型原生边界、母包/子包边界和长期记忆写入原则。
3. 全局理解：读 `AI_PROJECT_CONTEXT.md`。
4. 协同启动：读 `00.超级提示词工程/README.md`、`00.超级提示词工程/15-超级系统提示词工程/SUPER-SYSTEM-PROMPT-v3.0-AWAKENING.md` 和 `00.超级提示词工程/01-总控提示词/MASTER-ORCHESTRATOR-PROMPT.md`。
5. 模型边界：读 `00.超级提示词工程/11-模型原生协作协议/MODEL-NATIVE-COLLABORATION-PROTOCOL.md`，确认母包只提供项目上下文和证据链。
6. 唤醒握手：用 `00.超级提示词工程/12-引导秘书逻辑/MISSION-MEMORY-AWAKENING-PROTOCOL.md` 输出 `awakening_check`。
7. 入口判断：用 `00.超级提示词工程/12-引导秘书逻辑/GUIDE-SECRETARY-PROTOCOL.md` 先输出意图、置信度、路由、最小文件清单和验证计划。
8. 任务路由：用 `00.超级提示词工程/02-路由矩阵/SUBSYSTEM-ROUTING-MATRIX.md` 判断目标子系统，并回写 `route_feedback`。
9. 若任务是 PRD/SPEC、复杂功能、验收标准、需求变更或交付前规格冻结：进入 `00.超级提示词工程/06-原子化开发治理/SPECFORGE-PRD-SPEC-GATE.md`，把模糊需求锻造成可验证规格。
10. 若任务是 Skill、MCP、插件、LSP、开源库、脚本或工作流选型/配置/集成：进入 `00.超级提示词工程/10-通用AI协作生态/SKILL-CONFIGURATION-GATE.md`，先判断母包已有能力，再做候选评估、能力卡、配置和集成测试。
11. 若任务是使命、长期记忆、唤醒、身份逻辑、元智核：进入 `MISSION-MEMORY.md`、`00.超级提示词工程/12-引导秘书逻辑/MISSION-MEMORY-AWAKENING-PROTOCOL.md` 和 `00.超级提示词工程/13-源提示词吸收与演化/META-INTELLIGENCE-CORE-SUPER-PROMPT-DECONSTRUCTION.md`。
12. 若任务是完整阅读、全链路审计、齿轮咬合、数据/业务/运行/记忆/交付工作流对齐：进入 `00.超级提示词工程/14-全链路审计与运行对齐/`，先建立事实基线，再标注缺口。
    - 对跨文件夹任务，必须用 `UNIFIED-STATUS-OBJECT-SPEC.md` 生成或更新 `UNIFIED-STATUS-LEDGER.yaml` 中的状态对象。
    - 若任务涉及断裂点、路由反馈、暂停/阻塞状态或记忆源冲突，必须读取 `BREAKPOINT-REPAIR-MATRIX.md` 与 `MEMORY-SOURCE-INDEX.yaml`。
13. 若任务是吸收历史超级提示词、使用经验或失败案例：进入 `00.超级提示词工程/13-源提示词吸收与演化/`，先批判性转译，不把旧提示词原样提升为系统规则。
14. 若任务是平台开发：进入 `05.超极智脑_Q-SpecTrum`，读 `INDEX.md`、`AGENTS.md`、`智腦協議-BRAIN-PROTOCOL.md`，跑 `python verify-integration.py`。
15. 若任务是知识库/文件整理/MCP：进入 `03.数据库管理_文件夹整理AI应用`，读 `AGENTS.md`，跑 `python verify_install.py`。
16. 若任务是协议/SDK/部署：进入 `01.通讯协议_幽灵通道`，读 `00_总览/PROJECT_HANDOFF.md` 和对应 SDK README。
17. 若任务是 QCM 理论/公式/涌现：进入 `04.QCM-MVP-Emergence`，读 `PROJECT_HANDOFF-QCM.md`、`22_FORMULA_SYSTEM.md`、`qcm/pipeline.py`。
18. 修改前先确认子仓库 git 状态；不要把 `01/04` 的嵌入式副本误当成 `05` 的主运行时。
19. 若任务是最终交付：进入 `协同通用AI大模型开发交付包/`，先补齐价值体系、功能体系、结构体系、运作体系，再运行 `VERIFY-DELIVERY.ps1`；模板态可用普通模式，正式交付必须用 `-Strict` 模式通过后再压缩交付。

## 6. 当前已知风险/待清理点

| 项 | 风险 | 建议 |
|---|---|---|
| `01` 验证语义混淆 | `VERIFY.ps1` 是 manifest 完整性校验；SDK 测试需要另跑三组 pytest | 在验证登记表中分开 integrity 与 SDK tests |
| `01` 多份审计报告时间线不一致 | 早期报告说企业 SDK 待修，当前 pyproject 已修 | 后续以 `PROJECT_HANDOFF.md` 和实际 pyproject 为准 |
| `01/ghost-channel-sdk` 文档 import 示例漂移 | 使用者可能导入错包 | 统一为 `ghost_channel_sdk` |
| `02` 模板定位可能被过度承诺 | B6 已明确 template 定位、补 `.gitkeep`、PowerShell 命令和 tempdir smoke | 后续运行诉求默认路由到 03，除非明确要把 02 独立产品化 |
| `04` 旧 CLI 文档 | B4 已统一当前入口并保留旧参数排错提示 | 后续只在真实失败场景下复核 |
| `04/health_check.py` 历史结论已漂移 | 旧审计曾记录 4/6 NEEDS ATTENTION，当前实测 6/6 READY | 以后以当前命令输出和 `VALIDATION_REGISTRY.yaml` 为准 |
| `05/run.py --status` Windows 输出 | 旧版在 GBK 终端会被 emoji 打断 | 当前已做 UTF-8 输出硬化；仍建议保留状态命令在验证环中 |
| `05` 依赖说明冲突 | requirements、pyproject、README、QUICK-START、INSTALL-GUIDE 已对齐 | 后续若新增依赖，同步更新这些入口 |
| 根目录 Git Monorepo | 03/05为submodule，修改后需分别在子模块内commit，再更新根目录引用 | 修改前先 `git status` 确认所在层级 |

## 7. 最短启动命令清单

```powershell
# 01 通讯协议：完整性 + 三组 SDK 测试
cd "<母交付包根目录>\01.通讯协议_幽灵通道"
powershell -ExecutionPolicy Bypass -File .\VERIFY.ps1
python -m pytest "03_SDK与集成\02_开源社区包\ghost_channel开源库\tests" -q
python -m pytest "03_SDK与集成\04_SDK工程包\ghost-channel-sdk\python\tests" -q
python -m pytest "03_SDK与集成\03_企业SDK包\GhostHub_SDK\tests" -q

# 02 知识库模板：MemoryOS smoke
cd "<母交付包根目录>\02.通用知识库框架_Universal-KB"
python -m py_compile "04-memory\memoryos.py"
python "04-memory\memoryos.py"

# 03 知识库应用
cd "<母交付包根目录>\03.数据库管理_文件夹整理AI应用"
python verify_install.py
python app.py --port 5000

# 04 QCM MVP
cd "<母交付包根目录>\04.QCM-MVP-Emergence"
python "02-代码编写\test_qcm_all.py"
pytest "02-代码编写\test_roles.py" "02-代码编写\test_collaboration.py" "02-代码编写\test_sandbox.py" "02-代码编写\test_flywheel.py" "02-代码编写\test_summoning.py" -q

# 05 Q-SpecTrum 主平台
cd "<母交付包根目录>\05.超极智脑_Q-SpecTrum"
python verify-integration.py
$env:PYTHONUTF8='1'; python run.py --status
python run.py --web
```

## 8. CI/CD 与自动化

GitHub Actions 工作流位于 `.github/workflows/validate.yml`，每次 push 到 main 或 PR 时自动运行：

- **validate Job** (ubuntu-latest, Python 3.13/3.14)：qa_runner.py validate/status、Markdown fence 检查、submodule 状态检查
- **powershell-verify Job** (windows-latest)：`VERIFY-DELIVERY.ps1 -Strict` 交付验证

## 9. 开发迭代记录

| 阶段 | Commit 范围 | 主要成果 |
|------|-------------|----------|
| D (交付门禁) | b46c207 → 05a8147 | GitHub 创建、submodule push、根指针 commit |
| P1 (验证消除) | f683678 → 5ae25dc | venv 路由、SDK PYTHONPATH、MANIFEST 重生成、UTF8 编码、四体系填充、5 缺失文件 |
| P2 (架构提升) | 711e3e4 → 6ccb664 | QCM config 化 60 常量、源提示词吸收验证、AKU-SPEC、TRACEABILITY 实例、02 升级、CI/CD pipeline、.gitignore |
| R1 (飞轮) | f5fba1c | 45 专家名统一、SA 编号映射、commit 数校正、MASTER 12→15 模块、启动序列 1-17、LEDGER 11 对象 |
| R2 (飞轮) | 219c6d3 | P0-3 MASTER 15 模块引用、P1-4 启动序列重编号、P1-3 LEDGER 扩充 |
| R3 (飞轮) | b60edb1 | 全量验证 + 飞轮报告 v3.0-final |
| v3.1 (审计) | f7c250d → ef79aec | README/LICENSE 创建、文件数口径统一、飞轮报告 14 项事实核查 |

## 10. 工作原则

- 先分清“权威运行时”和“归档/副本/旧报告”。
- 文档声明与实际脚本冲突时，以当前代码、当前验证输出、当前 DB 查询为准。
- 修改 `03` 或 `05` 前先看各自 `AGENTS.md`；修改 `05` 前尤其先看 `_HANDOFF`。
- 未来若要把这些项目真正串成一个产品，优先从 `05` 做集成主线，`01` 提供通信协议，`03` 提供知识库/MCP 能力，`04` 提供 QCM 理论与公式模块。
