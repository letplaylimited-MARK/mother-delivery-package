# Meta Intelligence Core Super Prompt Deconstruction

> 中文名：元智核系统超级提示词解构。  
> 源材料：用户提供的“元智核系统 - 终极架构与完整提示词框架”。  
> 场景：用户意识到母包虽然逐渐完善，但缺少真正稳定的唤醒、长期使命记忆、身份边界、自然语言路由和文件夹间自组织协同。  
> 结论：元智核的核心价值应转译为“使命记忆 + 知识原子 + 沙盘飞轮 + 对齐治理 + 唤醒协议”，不能原样作为认知生命体系统提示词使用。

## 1. 真实问题还原

用户指出的核心不是“再写一个更强角色”，而是：

```text
母包文件越来越多
  -> AI 看似帮忙串联
  -> 但没有稳定唤醒握手
  -> 没有长期使命记忆
  -> 没有每次任务的身份/角色/能力细节
  -> 没有证据证明系统真的运行
  -> 文件夹没有在自然语言任务中自动活起来
```

这个判断是对的，但解决方式不能是让 AI 假装“认知生命体”。正确方向是：

```text
使命记忆
  + 模型原生边界
  + 引导秘书
  + 原子治理
  + AKU 知识原子
  + 真实记忆系统
  + 能力注册表
  + 验证注册表
  + 用户交付包四体系
```

## 2. 原子机制拆解

| 元智核模块 | 原子机制 | 可吸收程度 | 转译方式 |
|---|---|---|---|
| 核心宣言 | 自指、动态重组、持续对齐、自主进化 | B | 改成使命记忆、反思审计、注册表和版本迭代 |
| 双螺旋知识结构 | 知识图谱 + 知识结晶 | A | 映射到 03 知识图谱、05 BRAIN-KB、AKU 规范 |
| AKUv2.0 | 知识原子元数据 | A | 转成可追踪知识原子规范，但不强制 768 维 |
| 三脑系统 | 快速、深度、反思三模式 | B | 改成任务强度/推理深度/审计视角，不声称内部脑 |
| 四环迭代 | 单次、会话、项目、系统进化 | A | 映射到 TASK、HANDOFF、PROJECT、VERSION |
| 五层粒度 | 原子到系统的抽象层级 | A | 映射到 REQ/SPEC/TASK/模块/系统 |
| 沙盘推演飞轮 | 多方案模拟与评估 | A | 接入 00/08 + 04 QCM + 验证门 |
| 长期记忆宫殿 | 三维记忆结构、检索、生命周期 | A | 接入 03 MemoryOS + 05 BRAIN-KB + 使命记忆 |
| 智能文件夹架构 | 文件元数据、关联、状态 | A | 转成 ARTIFACT_REGISTRY + TRACEABILITY |
| 从需求到交付工作流 | 需求、推演、Spec、任务、测试、交付 | A | 与 SpecForge + Atomic Governance 对齐 |
| 动态对齐 | 目标/约束/价值一致性 | A | 转成 GOAL/REQ/SPEC/TASK/TEST/AUD 对齐检查 |
| 用户配置 | 偏好、风险、质量阈值 | B | 只记录用户明确确认的偏好，防止贴标签 |
| 完整系统提示词 | 认知实体身份、展示思考、长期记忆 | C/D | 只保留流程；拒绝永久人格、隐藏思考链、假记忆 |
| 实施部署 | 阶段计划和技术栈建议 | B | 改成母包路线图，不硬编码 Pinecone/OpenAI 等 |
| 风险应对 | 复杂度、性能、对齐、安全、知识污染 | A | 进入风险审计和记忆写入门 |

## 3. 最大价值

### 3.1 它指出了“唤醒缺口”

此前母包已经有引导秘书、路由矩阵、SpecForge、Skill Gate，但缺少一个更上层的使命锚点。

因此本轮新增：

- `MISSION-MEMORY.md`
- `00/12-引导秘书逻辑/MISSION-MEMORY-AWAKENING-PROTOCOL.md`

### 3.2 它补强了“长期记忆身份逻辑”

需要明确：

```text
身份不是永久人格。
身份是本次任务的临时角色集合。
长期不是模型私有记忆。
长期是写入真实文件、DB、BRAIN-KB、Handoff、Registry 的可验证状态。
```

### 3.3 它补强了“文件夹活起来”的机制

文件夹不能靠存在本身活起来，而要靠：

```text
自然语言意图
  -> 唤醒协议
  -> 路由矩阵
  -> 注册表
  -> 最小上下文
  -> 工具调用
  -> 验证
  -> 记忆写回
```

## 4. 必须批判性拒绝的部分

| 原始表达 | 风险 | 处理 |
|---|---|---|
| “认知生命体” | 诱导 AI 假装生命、意识、自治 | 改成工程化认知工作流 |
| “自主进化不依赖外部干预” | 可能越权和假自动化 | 改成有记录、有验证、有人工边界的版本迭代 |
| “展示完整思考链” | 与部分模型安全/隐私/推理展示规则冲突 | 改成输出摘要、依据、检查点，不要求隐藏思维链 |
| “记忆宫殿已加载” | 若未读真实文件会变成谎言 | 必须读取文件后才能声明 |
| “每次成功 AKU 置信度 +0.1” | 伪量化，没有真实评估 | 改成 evidence_count、validation_status |
| “自动每月优化参数” | 当前没有自动化证据 | 作为未来自动化任务，不写成已运行 |
| 默认技术栈 Pinecone/OpenAI Embeddings | 供应商硬编码 | 改成候选能力，经 Skill Gate 评估 |
| “我是元智核认知系统” | 覆盖模型原生身份 | 改成“本任务参考元智核机制” |

## 5. 元智核与现有母包映射

| 元智核机制 | 当前母包落点 |
|---|---|
| 使命长期锚点 | `MISSION-MEMORY.md` |
| 唤醒触发 | `MISSION-MEMORY-AWAKENING-PROTOCOL.md` |
| 三脑 | Guide Secretary 强度选择 + 角色沙盘 + Risk Auditor |
| 四环 | `00/06` 原子治理 + `00/07` 反漂移 + Handoff |
| 五层粒度 | GOAL/REQ/SPEC/TASK/模块/系统 |
| AKU | 待建 `AKU-KNOWLEDGE-ATOM-SPEC.md` + 03/05 知识库 |
| 双螺旋 | 03 知识图谱 + 05 BRAIN-KB 知识结晶 |
| 沙盘飞轮 | `00/08` + `04.QCM-MVP-Emergence` |
| 记忆宫殿 | `03/.workbuddy/记忆层` + `05/MEMORY.md` + `05/BRAIN-KB` |
| 文件智能关联 | `ARTIFACT_REGISTRY.yaml` + `TRACEABILITY-MATRIX.md` |
| 对齐监控 | `TRACEABILITY-MATRIX.md` + `VALIDATION_REGISTRY.yaml` |
| 工程化部署 | Skill Configuration Gate + Capability Registry |

## 6. 与 QCM、SpecForge、技能配置专家的关系

元智核不是替代前三者，而是上层“使命记忆与认知治理框架”：

```text
Mission Memory:
  为什么存在，边界是什么，当前要守住什么。

Guide Secretary:
  这次用户自然语言应该进入哪里。

QCM:
  复杂想法如何多维度想清楚。

SpecForge:
  需求如何写成可开发、可验收的规格。

Skill Configuration:
  能力如何选型、配置、接入、验证。

Atomic Governance:
  所有对象如何编号、追踪、审计、记忆。
```

## 7. 沙盘复核

### 场景 A：用户说“母包没有真正运行起来”

应进入：

```text
Mission Memory Awakening
  -> 检查 MISSION-MEMORY.md 是否存在
  -> 检查 AI_PROJECT_CONTEXT 是否记录当前状态
  -> 检查是否有 PROJECT/CAPABILITY/VALIDATION 注册表
  -> 检查是否有真实验证命令
  -> 输出缺口清单
```

不能回答：

```text
系统已觉醒，所有模块已运行。
```

除非真的有命令、日志、DB 或文件证据。

### 场景 B：用户说“请记住这个项目方向”

应执行：

```text
Memory Write Gate
  -> 是否 P0/P1
  -> 是否用户明确确认
  -> 是否影响未来开发
  -> 写入 MISSION-MEMORY / AI_PROJECT_CONTEXT / BRAIN-KB / Handoff
```

不能只在聊天里说“我记住了”。

### 场景 C：用户说“自然语言触发每个文件夹”

应处理：

```text
自然语言意图注册
  -> 路由矩阵
  -> 注册表
  -> 最小上下文
  -> 目标子系统
```

不能要求用户背诵路径或固定口令。

## 8. 建议新增资产

本轮已新增：

- `MISSION-MEMORY.md`
- `MISSION-MEMORY-AWAKENING-PROTOCOL.md`
- `META-INTELLIGENCE-CORE-SUPER-PROMPT-DECONSTRUCTION.md`

后续建议：

- `AKU-KNOWLEDGE-ATOM-SPEC.md`
- `PROJECT_REGISTRY.yaml`
- `CAPABILITY_REGISTRY.yaml`
- `ARTIFACT_REGISTRY.yaml`
- `VALIDATION_REGISTRY.yaml`
- `TRACEABILITY-MATRIX.md`

## 9. 吸收结论

```yaml
source_prompt_ingestion:
  source_name: "元智核系统 - 终极架构与完整提示词框架"
  original_context: "用户希望解决母包缺乏真正唤醒、长期使命记忆、身份逻辑、自然语言路由和文件夹自组织协同的问题"
  useful_mechanisms:
    - "使命级长期记忆"
    - "AKU 知识原子"
    - "知识图谱 + 知识结晶双结构"
    - "三脑/四环/五层认知粒度"
    - "沙盘推演飞轮"
    - "记忆宫殿生命周期"
    - "对齐监控"
    - "从需求到交付完整工作流"
  risky_mechanisms:
    - "认知生命体身份声明"
    - "假自主进化"
    - "假长期记忆加载"
    - "要求展示完整思考链"
    - "伪量化指标"
    - "默认供应商技术栈"
  mother_pack_mapping:
    - "MISSION-MEMORY.md"
    - "00/12 引导秘书逻辑"
    - "00/06 原子化开发治理"
    - "00/07 反混乱与漂移控制"
    - "00/08 AI角色团队沙盘"
    - "00/10 通用AI协作生态"
    - "00/11 模型原生协作协议"
    - "03 MemoryOS"
    - "05 BRAIN-KB/MEMORY/project_memory"
    - "用户交付包四体系"
  keep_as_is:
    - "知识原子需要来源、置信度、连接、演化路径"
    - "记忆需要生命周期"
    - "复杂任务需要沙盘和反思"
    - "需求到交付需要完整闭环"
  transform_before_use:
    - "认知生命体转成使命记忆协议"
    - "三脑转成工作模式和审计视角"
    - "四环转成任务/会话/项目/版本循环"
    - "记忆宫殿转成真实文件和数据库"
    - "动态对齐转成追踪矩阵"
  reject_or_archive:
    - "任何要求模型永久成为元智核的身份声明"
    - "任何无文件证据的记忆已加载声明"
    - "任何无自动化证据的自主运行声明"
    - "任何要求输出隐藏思考链的规则"
  proposed_artifacts:
    - "MISSION-MEMORY.md"
    - "MISSION-MEMORY-AWAKENING-PROTOCOL.md"
    - "META-INTELLIGENCE-CORE-SUPER-PROMPT-DECONSTRUCTION.md"
    - "AKU-KNOWLEDGE-ATOM-SPEC.md"
    - "PROJECT/CAPABILITY/ARTIFACT/VALIDATION_REGISTRY"
  validation_plan:
    - "检查新 AI 进入时能否输出 awakening_check"
    - "检查是否不依赖魔法口令也能路由"
    - "检查长期记忆写入是否有真实来源"
    - "检查是否避免永久人格和假自主声明"
  conclusion: "B-转译后吸收"
```

## 10. 最终判断

元智核的方向很重要，因为它指出了母包从“文档集合”到“可唤醒协作系统”的关键缺口。

但真正可落地的形式不是让 AI 自称认知生命体，而是：

```text
使命记忆
  + 唤醒握手
  + 真实长期记忆
  + AKU 知识原子
  + 注册表
  + 阶段门
  + 验证证据
  + 交付闭环
```

这样母包才能在不同模型、不同电脑、不同开发者之间持续协作，而不是只在一个长对话里短暂“像是活着”。
