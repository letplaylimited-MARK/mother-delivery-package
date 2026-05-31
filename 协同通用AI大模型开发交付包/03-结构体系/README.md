# 结构体系

> 用途：说明项目由哪些文件、模块、数据、接口、依赖组成，方便用户、开发者和 AI 快速理解。
> 生成时间：2026-05-31，基于母交付包实际目录结构、审计清单与运行验证。

## 1. 目录地图

```text
project-root/
├── MISSION-MEMORY.md                          # 母包使命、身份边界、唤醒握手
├── AI_PROJECT_CONTEXT.md                      # 全局目录地图、子系统定位
├── MOTHER-PACK-ACTIVATION-GUIDE.md            # 唯一权威 AI 启动协议
├── 开发者母交付包使用说明.md                    # 开发者入门指南
├── qa_runner.py                               # 31 项注册验证统一入口
├── qcm-universal-ai-system-v3.0.skill          # QCM 技能文件（ZIP，45 角色/9 阶段）
├── .gitignore                                 # Git 排除规则
│
├── 00.超级提示词工程/                           # 跨项目 AI 协同的提示词操作系统与审计控制平面
│   ├── 01-总控提示词/                           # AI 进入后的启动逻辑
│   ├── 02-路由矩阵/                             # 子系统路由判断
│   ├── 03-上下文包模板/                         # 任务上下文装配
│   ├── 04-协同工作流/                           # 跨项目工作流
│   ├── 05-评估与迭代/                           # 输出质量评估
│   ├── 06-原子化开发治理/                       # GOAL/REQ/PRD/SPEC/TASK/TEST/AUD/MEM
│   ├── 07-反混乱与漂移控制/                     # 需求/规格/语义漂移防护
│   ├── 08-AI角色团队沙盘/                      # 多角色协作推演
│   ├── 09-母包集成蓝图/                         # 母包整体协同蓝图
│   ├── 10-通用AI协作生态/                       # Skill/MCP/LSP/插件接入
│   ├── 11-模型原生协作协议/                     # 模型规则优先声明
│   ├── 12-引导秘书逻辑/                         # 意图识别/路由/交接
│   ├── 13-源提示词吸收与演化/                   # 四套历史源提示词解构与转译
│   ├── 14-全链路审计与运行对齐/                 # 注册表/审计/断裂点/状态账本
│   └── 15-超级系统提示词工程/                   # SSP v1/v2/v3 + 沙盘报告
│
├── 01.通讯协议_幽灵通道/                        # Ghost Channel v1.0 协议+SDK（299 manifest checked）
│   ├── 00_总览/                                # 项目总览和交接
│   ├── 01_核心协议/                             # Delta/VectorClock/Merkle/AES/HMAC
│   ├── 02_开源社区包/                           # ghost_channel 开源 SDK（18 tests）
│   ├── 03_SDK与集成/                            # 企业 SDK + 轻量 SDK + 测试
│   ├── 04_企业部署/                             # Docker/K8s/授权/监控
│   ├── VERIFY.ps1                              # 完整性验证脚本
│   └── MANIFEST.yaml                           # 299 文件 SHA256 完整性清单
│
├── 02.通用知识库框架_Universal-KB/              # Universal-KB 模板规范（当前审计 22 文件）
│   └── 01-raw -> 02-processed -> 03-wiki -> 04-memory -> 05-agents -> 06-output
│
├── 03.数据库管理_文件夹整理AI应用/               # V2 知识库应用（当前审计 153 文件，子工作区）
│   ├── app.py                                  # Flask Web/REST/CLI（端口 5000）
│   ├── mcp_server.py                           # MCP Server（20 个工具）
│   ├── tests/                                  # 当前审计 107 tests
│   └── verify_install.py                       # 安装验证（23 通过 / 0 失败）
│
├── 04.QCM-MVP-Emergence/                       # QCM 共鸣/涌现 MVP（当前审计 148 文件）
│   ├── 02-代码编写/                             # 22 公式实现 + 测试
│   ├── qcm/                                    # 命名空间包（config/core/roles/collaboration）
│   └── test_qcm_all.py                         # 25/25 tests 通过
│
├── 05.超极智脑_Q-SpecTrum/                      # 主平台（当前审计 423 文件，子工作区）
│   ├── qspectrum_engine.py                     # 主引擎（Secretary->KnowledgeResonance->LLM）
│   ├── api_server.py                           # REST API + Web UI（端口 8765）
│   ├── run.py                                  # CLI/Web/status 统一入口
│   ├── brain_core/                             # 可复用脑模块（config/graph/MCP/capabilities）
│   ├── BRAIN-KB/                               # P0-P1 长期知识
│   ├── verify-integration.py                   # 结构集成验证
│   └── AI项目管理/Platform/db/platform.db       # 平台数据库权威位置（15 角色）
│
└── 协同通用AI大模型开发交付包/                    # 用户交付包（本目录）
    ├── README.md                               # 交付包说明
    ├── 交付包组装规则.md                         # 三层级交付规范
    ├── VERIFY-DELIVERY.ps1                     # 交付验证脚本（普通/严格模式）
    ├── AI_PROJECT_CONTEXT.md                   # 项目上下文（交付给用户的版本）
    ├── CHANGELOG.md                            # 变更日志
    ├── HANDOFF.md                              # 交接文档
    ├── TRACEABILITY-MATRIX.md                  # 追踪矩阵
    ├── VALIDATION_REPORT.md                    # 验证报告
    ├── 01-价值体系/                             # 为什么值得交付
    ├── 02-功能体系/                             # 项目能做什么
    ├── 03-结构体系/                             # 由哪些模块组成
    └── 04-运作体系/                             # 如何安装/启动/维护
```

## 2. 模块职责

| 模块 | 职责 | 上游 | 下游 |
|---|---|---|---|
| 00 超级提示词工程 | 控制平面：启动/路由/阶段门/审计/记忆写入规则 | MISSION-MEMORY.md | 所有子系统 |
| 01 幽灵通道 | 通信协议层：多智能体同步/加密/完整性/审计 | 无（独立协议） | 05 Q-SpecTrum、04 QCM |
| 02 通用知识库 | 知识管理模板：目录范式/MemoryOS | 无（独立模板） | 03 知识库应用 |
| 03 数据库管理 | 知识库应用层：Flask Web/MCP/向量检索/文件整理 | 02 模板 | 05 Q-SpecTrum |
| 04 QCM-MVP | 理论验证层：共鸣公式/涌现检测/沙盘/飞轮 | 01 协议副本 | 05 Q-SpecTrum |
| 05 Q-SpecTrum | 集成平台层：角色/知识/协议/Web/API/MCP/闭环 | 01/03/04 全部 | 最终用户 |
| 协同交付包 | 交付层：四体系/验证/交接 | 05 全部子系统产出 | 最终用户/运维者 |

## 3. 数据流

```text
用户自然语言输入
  -> 引导秘书（意图识别 + 5D 雷达 + 置信度评估）
  -> 路由矩阵（子系统选择 + route_feedback）
  -> 子系统执行
    -> SpecForge（需求 -> PRD/SPEC/TEST）
    -> QCM（角色协同 -> R 值 -> 涌现检测）
    -> 知识库（文件/知识 -> 向量索引 -> 检索）
    -> Ghost Channel（多 Agent -> 同步/加密/审计）
    -> Q-SpecTrum（统一调度 + Web UI + API）
  -> 原子治理（TASK/TEST/AUD/MEM 追踪）
  -> 验证证据链（qa_runner.py validate）
  -> 用户交付包（四体系 + VERIFY-DELIVERY.ps1 -Strict）
```

## 4. 接口与集成

| 接口 | 类型 | 调用方 | 返回/效果 |
|---|---|---|---|
| `qa_runner.py validate` | CLI | 开发者/AI | 31 项注册验证结果（PASS/FAIL/WARN/SKIP） |
| `03/mcp_server.py` | MCP stdio | AI 模型 | 20 个工具（搜索/向量/记忆/文件处理/工作流） |
| `05/api_server.py` | REST API | Web 前端/脚本 | `/api/chat`、roles、knowledge、memory 等端点 |
| `05/run.py` | CLI | 开发者 | `--web`(Web UI)、`--status`(健康检查)、`--query`(查询) |
| `03/app.py` | Flask CLI | 开发者 | `--port`(Web 服务)、搜索/浏览/ingest/memory 子命令 |
| `01/VERIFY.ps1` | PowerShell | qa_runner.py | MANIFEST 完整性校验（299 文件 SHA256） |
| `VERIFY-DELIVERY.ps1` | PowerShell | 开发者 | 交付包验证（普通/严格模式） |
| `validate_consistency.py` | Python | 开发者/AI | 10 维跨文档一致性检查 |

## 5. 依赖与配置

| 类型 | 内容 | 说明 |
|---|---|---|
| 运行时 | Python 3.10+ | 推荐 venv 隔离；当前验证环境为 Python 3.14.4，ChromaDB 有外部弃用警告但测试通过 |
| Python 包 | cryptography, Flask, numpy, chromadb, pytest, pytest-asyncio 等 | 以各子系统 `requirements.txt` / `pyproject.toml` 为准 |
| 数据库 | SQLite（platform.db、search_index.db） | 05 和 03 的运行时数据库 |
| 向量检索 | ChromaDB | 03 知识库和 05 Q-SpecTrum 的向量搜索 |
| 版本控制 | Git（Monorepo + 2 Submodule） | 03→knowledge-base-manager(main), 05→Q-Spectrum(master) |
| 模型/API | 通用 AI 大模型（用户自备 API Key） | 不硬编码特定模型，支持任意通用 AI |

## 6. 构建与产物

| 产物 | 生成方式 | 用途 |
|---|---|---|
| `qcm-universal-ai-system-v3.0.skill` | 打包生成（ZIP 357KB） | QCM 技能定义，45 角色/9 阶段/24 维/5 子代理 |
| `01/MANIFEST.yaml` | Python 脚本自动生成 | 299 文件 SHA256 完整性清单 |
| 验证报告 | `qa_runner.py validate` | 31 项注册验证结果，JSON 结构化输出 |
| 交付包验证结果 | `VERIFY-DELIVERY.ps1 [-Strict]` | 交付就绪度检查 |
| Git 仓库 | `git push origin main` | GitHub: letplaylimited-MARK/mother-delivery-package |
