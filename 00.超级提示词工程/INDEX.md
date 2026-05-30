# 00.超级提示词工程 -- INDEX

> 定位: 跨项目 AI 协同的提示词操作系统 -- 所有子系统的元控制层

## 文件结构
```
00.超级提示词工程/
├── README.md
├── 01-总控提示词/          MASTER-ORCHESTRATOR-PROMPT.md
├── 02-路由矩阵/            SUBSYSTEM-ROUTING-MATRIX.md
├── 03-上下文包模板/        AI-CONTEXT-PACK-TEMPLATE.md
├── 04-协同工作流/          CROSS-PROJECT-WORKFLOW.md
├── 05-评估与迭代/          PROMPT-EVALUATION-RUBRIC.md
├── 06-原子化开发治理/      3 文件 (SPECFORGE / TRACEABILITY / ATOMIC-OS)
├── 07-反混乱与漂移控制/    ANTI-DRIFT-PROTOCOL.md
├── 08-AI角色团队沙盘/      2 文件 (SANDBOX / REPLAY)
├── 09-母包集成蓝图/        MOTHER-PACK-AI-COLLABORATION-BLUEPRINT.md
├── 10-通用AI协作生态/      3 文件 (ECOSYSTEM / CONTRACT / SKILL-GATE)
├── 11-模型原生协作协议/    MODEL-NATIVE-COLLABORATION-PROTOCOL.md
├── 12-引导秘书逻辑/        3 文件 (GUIDE / HANDOFF / AWAKENING)
├── 13-源提示词吸收与演化/  6 文件 (INGESTION / 4 DECONSTRUCTION / REVIEW)
└── 14-全链路审计与运行对齐/ 12 文件 (6 审计文档 + 6 Registry YAML)
```

## 关键入口
| 文件 | 用途 | 优先级 |
|------|------|--------|
| 01-总控提示词/MASTER-ORCHESTRATOR-PROMPT.md | AI 会话启动入口，装配全局上下文 | 高 |
| 02-路由矩阵/SUBSYSTEM-ROUTING-MATRIX.md | 判断用户任务归属哪个子系统 | 高 |
| 03-上下文包模板/AI-CONTEXT-PACK-TEMPLATE.md | 组装最小必要上下文 + 绑定追踪 ID | 高 |
| 12-引导秘书逻辑/GUIDE-SECRETARY-PROTOCOL.md | 意图识别、澄清、路由、交接 | 高 |
| 12-引导秘书逻辑/MISSION-MEMORY-AWAKENING-PROTOCOL.md | 使命唤醒，自然语言触发判断 | 高 |
| 06-原子化开发治理/SPECFORGE-PRD-SPEC-GATE.md | PRD/SPEC 锻造门 | 中 |
| 11-模型原生协作协议/MODEL-NATIVE-COLLABORATION-PROTOCOL.md | 声明母包不覆盖模型自身系统逻辑 | 中 |
| 14-全链路审计与运行对齐/ | 6 审计文档 + 6 Registry YAML | 中 |

## 快速导航

新 AI/新会话进入时的最小必读路径:

1. 根目录 MISSION-MEMORY.md -- 确认母包使命与身份边界
2. 根目录 AI_PROJECT_CONTEXT.md -- 项目上下文地图
3. 本目录 README.md -- 设计原则与闭环
4. 01-总控提示词/ -- 启动逻辑
5. 11-模型原生协作协议/ -- 模型边界声明
6. 12-引导秘书逻辑/MISSION-MEMORY-AWAKENING-PROTOCOL.md -- 使命唤醒
7. 12-引导秘书逻辑/GUIDE-SECRETARY-PROTOCOL.md -- 意图识别与路由
8. 02-路由矩阵/ -- 子系统归属判断

核心闭环: 意图识别 -> 子系统路由 -> 上下文装配 -> 任务执行 -> 验证 -> 交接 -> 记忆沉淀
