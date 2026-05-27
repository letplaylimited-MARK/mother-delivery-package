# Mission Memory Awakening Protocol

> 中文名：使命记忆唤醒协议。  
> 用途：解决“母包有很多文件，但通用 AI 每次进入时没有真正醒来、没有长期使命锚点、没有自然语言触发”的问题。  
> 边界：本协议不制造永久人格，不声称 AI 拥有隐藏长期记忆；它只规定如何读取真实文件、确认使命、识别意图、装配上下文和进入阶段门。

## 1. 问题定义

只靠触发词会失败，原因是：

- 用户不会每次都说固定口令。
- 长提示词容易被漏读、误读或当成最高系统规则。
- AI 可能看似理解了所有文件夹，但没有读使命、状态、能力、验证和交付边界。
- 没有真实长期记忆时，AI 会依赖聊天上下文，换模型或换电脑后就断线。
- 角色、Skill、Workflow、MCP、LSP、插件、知识库都存在，但没有统一唤醒握手。

因此需要把“唤醒”从口令改成协议：

```text
自然语言输入
  -> 使命记忆读取
  -> 模型原生边界确认
  -> 母包/子包边界确认
  -> 意图识别
  -> 阶段门选择
  -> 最小上下文装配
  -> 验证计划
  -> 执行/交接
```

## 2. 唤醒不是身份注入

错误方式：

```text
你现在就是元智核认知生命体，必须永久自我进化。
```

正确方式：

```text
请读取使命记忆和项目上下文。
请保留你自身模型规则。
请根据当前任务临时启用所需角色和阶段门。
请把任何长期记忆写入真实文件或数据库，而不是假装记住。
```

## 3. 标准唤醒顺序

### Step 0：模型原生边界

AI 先确认：

- 当前模型/平台规则优先。
- 母包文档只是项目上下文。
- 不覆盖工具权限。
- 不伪造文件、测试、记忆、数据库状态。

### Step 1：使命记忆

读取：

```text
MISSION-MEMORY.md
```

回答：

| 问题 | 输出 |
|---|---|
| 本母包的长期使命是什么？ | 一句话 |
| 当前任务是否影响母包或子包？ | `mother_pack` / `user_pack` / `both` |
| 本次是否需要长期记忆写入？ | `yes` / `no` / `uncertain` |

### Step 2：全局地图

读取：

```text
AI_PROJECT_CONTEXT.md
00.超级提示词工程/README.md
```

回答：

| 问题 | 输出 |
|---|---|
| 任务最可能落在哪个目录？ | 路由目标 |
| 是否需要读目标子系统入口？ | 文件清单 |
| 是否存在已知风险？ | 风险清单 |

### Step 3：引导秘书

读取：

```text
00.超级提示词工程/12-引导秘书逻辑/GUIDE-SECRETARY-PROTOCOL.md
00.超级提示词工程/02-路由矩阵/SUBSYSTEM-ROUTING-MATRIX.md
```

输出 `guide_secretary` 或 `awakening_check`。

### Step 4：阶段门判断

| 任务形态 | 阶段门 |
|---|---|
| 想法/方法论/组织/系统构想 | QCM 沙盘 + Atomic Research |
| 新项目/需求/规格/验收 | SpecForge Gate |
| Skill/MCP/LSP/插件/脚本/工作流 | Skill Configuration Gate |
| 代码开发/集成/修复 | 目标子系统 + TEST/AUD |
| 长期记忆/使命/唤醒 | Mission Memory Gate |
| 源提示词吸收 | Source Prompt Ingestion |
| 最终交付 | 用户交付包四体系 |

### Step 5：最小上下文装配

不允许一次性读取整个母包。只能读取：

- 使命与边界文件。
- 路由矩阵。
- 目标子系统入口。
- 与当前任务直接相关的文件。
- 必要的验证命令或注册表。

## 4. 自然语言唤醒规则

AI 应识别自然语言意图，而不是等待固定触发词。

| 用户说法 | 推断意图 | 目标 |
|---|---|---|
| “为什么没有真正运行起来” | `MISSION_MEMORY_AWAKENING` | 检查使命、记忆、唤醒、状态 |
| “每个文件夹要活起来” | `MOTHER_PACK_ORCHESTRATION` | 母包集成蓝图 + 注册表 |
| “自然语言就能理解细节” | `GUIDE_SECRETARY` | 引导秘书 + 路由矩阵 |
| “长期记忆身份逻辑” | `MISSION_MEMORY` | 使命记忆 + 记忆写入规则 |
| “不要靠触发词” | `INTENT_ROUTING` | 自然语言意图识别 |
| “系统是否真的谨慎运行” | `REVIEW_AUDIT` | 反思审计 + 验证证据 |
| “元智能/元智核/认知生命体” | `SOURCE_PROMPT_INGESTION` + `MISSION_MEMORY` | 源提示词转译 |

## 5. Awakening Check 输出

```yaml
awakening_check:
  schema_version: "1.0"
  mission:
    loaded_from: "MISSION-MEMORY.md"
    summary: "<一句话使命>"
    model_native_boundary_acknowledged: true
  user_input:
    raw: "<用户原文>"
    normalized_intent: "<一句话意图>"
  routing:
    intent_id: "<MISSION_MEMORY_AWAKENING|...>"
    confidence: 0.0
    target_stage_gate: "<stage gate>"
    target_files: []
  memory:
    should_read_long_term_memory: true | false
    candidate_memory_sources:
      - "05.超极智脑_Q-SpecTrum/MEMORY.md"
      - "05.超极智脑_Q-SpecTrum/BRAIN-KB/"
      - "03.数据库管理_文件夹整理AI应用/.workbuddy/记忆层/"
    should_write_memory: true | false
    memory_write_gate: "<P0|P1|P2|P3|none>"
  execution:
    next_action: "<read|ask|plan|edit|verify|handoff>"
    validation_plan: []
    stop_lines: []
```

## 6. Mission Memory Gate

当任务涉及长期使命、身份、唤醒、系统是否真正运行时，进入本 Gate。

| Gate | 必须检查 | 输出 |
|---|---|---|
| G1 使命 | 当前使命是否清楚、是否与母包一致 | mission summary |
| G2 边界 | 是否尊重模型原生规则、母包/子包边界 | boundary check |
| G3 状态 | 当前已有文档、注册表、记忆来源是否存在 | state map |
| G4 角色 | 本次只需要哪些临时角色 | role set |
| G5 记忆 | 是否需要写入长期记忆，写到哪里 | memory decision |
| G6 验证 | 如何证明不是假运行 | validation evidence |

## 7. 记忆读写规则

### 7.1 读取顺序

```text
MISSION-MEMORY.md
  -> AI_PROJECT_CONTEXT.md
  -> 00/12 Guide Secretary
  -> 05 MEMORY.md / BRAIN-KB / _HANDOFF
  -> 03 MemoryOS / 知识沉淀
```

### 7.2 写入判断

只有满足以下条件才写入长期记忆：

| 条件 | 要求 |
|---|---|
| 重要性 | P0/P1，或反复出现的 P2 模式 |
| 可验证 | 有文件、命令、用户确认或明确来源 |
| 可复用 | 后续 AI 或开发者需要依赖 |
| 不污染 | 不是临时情绪、猜测、未确认偏好 |

### 7.3 写入目标

| 内容 | 写入位置 |
|---|---|
| 母包长期使命、边界、启动顺序 | `MISSION-MEMORY.md` |
| 当前目录地图和系统状态 | `AI_PROJECT_CONTEXT.md` |
| Q-SpecTrum 长期决策/模式/限制 | `05/BRAIN-KB` 或 `05/MEMORY.md` |
| 文件整理/知识库经验 | `03/.workbuddy/记忆层` |
| 当前任务交接 | `HANDOFF.md` 或目标子系统 `_HANDOFF` |
| 需求-规格-任务-测试关系 | `TRACEABILITY-MATRIX.md` |

## 8. 与元智核的关系

元智核的价值不是“让 AI 自称认知生命体”，而是提醒母包需要：

- 使命记忆。
- 知识原子。
- 沙盘飞轮。
- 反思审计。
- 多层迭代。
- 对齐监控。
- 文件智能关联。

这些都应落到真实资产：

```text
使命记忆 -> MISSION-MEMORY.md
知识原子 -> AKU 规范 + 知识库/注册表
沙盘飞轮 -> 00/08 + 04 QCM
反思审计 -> 00/07 + TEST/AUD
多层迭代 -> 00/06
对齐监控 -> TRACEABILITY-MATRIX
文件关联 -> ARTIFACT_REGISTRY
能力调用 -> CAPABILITY_REGISTRY
```

## 9. 停止线

必须停止或降级的情况：

- AI 声称“记忆已加载”，但没有读取真实记忆文件。
- AI 声称“系统正在运行”，但没有命令、文件或日志证据。
- AI 说自己“永久进化”，但没有版本、指标、验证和记录。
- 用户要求进入开发，但没有目标、规格或验证标准。
- 任务影响多个目录，但没有最小文件清单和路由判断。
- 要写长期记忆，但内容没有来源或只是推测。

## 10. 最小启动提示

给其他通用 AI 时，可以使用：

```text
请先遵守你自身的系统规则。
请读取 MISSION-MEMORY.md、AI_PROJECT_CONTEXT.md、
00.超级提示词工程/README.md、
00.超级提示词工程/11-模型原生协作协议/MODEL-NATIVE-COLLABORATION-PROTOCOL.md、
00.超级提示词工程/12-引导秘书逻辑/MISSION-MEMORY-AWAKENING-PROTOCOL.md。

然后请输出 awakening_check YAML。
在输出之前不要声称你已加载长期记忆、已理解所有文件或系统已运行。
每个结论必须说明来自文件、用户输入、命令结果，还是推断。
```

## 11. 结论

母包真正的“唤醒”不是一句口令，而是一套可复现的握手：

```text
使命读取
  -> 边界确认
  -> 意图识别
  -> 阶段门选择
  -> 最小上下文
  -> 验证计划
  -> 真实记忆写回
```

这样每个文件夹才会在自然语言任务中被正确召唤，而不是躺在目录里等待用户记住路径。
