# 母交付包 AI 激活引导

> Mother Package AI Activation Guide
> 用途: 让一个全新AI首次接收母交付包压缩包后, 正确完成唤醒、路由、协同开发
> 受众: 开发者(本节) + AI(下一节)

---

## ═══ 人类设置指南 ═══

### 你需要什么

- 母交付包文件夹(已解压), 或 GitHub 仓库地址
- 一个 AI 对话窗口: 支持 System Prompt 最好; 只支持普通聊天也可以
- 新环境必须使用 `git clone --recurse-submodules` 或 `git submodule update --init --recursive`
- 若要修改 `03` 或 `05` 子仓库, fresh clone 后需先在子仓库内切换分支: `03 -> main`, `05 -> master`

### Step 1: 选择启动模式

#### 模式 A: System Prompt 模式

打开 `00.超级提示词工程/15-超级系统提示词工程/SUPER-SYSTEM-PROMPT-v3.0-AWAKENING.md`
将其**全部内容**复制到AI的**系统提示词(System Prompt)**输入框。

这是AI的"引导加载器"内核(~9KB), 包含:
- 根目录定位逻辑 + 简单查询快速通道
- 15模块+7子系统的常驻系统拓扑地图
- 12条反幻觉铁律(MUST NOT)

#### 模式 B: 普通聊天框模式

如果新的 AI 工具没有 System Prompt 输入框, 打开:

`00.超级提示词工程/15-超级系统提示词工程/FIRST-DIALOG-BOOTSTRAP-PROMPT.md`

将其中 **"可复制首条消息"** 代码块完整发送给新 AI。该消息会要求新 AI 完成 clone、submodule、读取、验证、路由和 `cold_start_report`。

普通聊天框模式采用 6 阶段门: P0 Boundary、P1 Integrity、P2 Validation、P3 Routing、P4 Execution Eligibility、P5 Handoff。只有 `P4_execution_eligibility` 不是 BLOCKED 时, 才允许进入编辑或执行。

### Step 2: 启动对话

模式 A 发送第一条消息(逐字):

> 请读取根目录的 MOTHER-PACK-ACTIVATION-GUIDE.md 并完成唤醒激活

模式 B 已在 `FIRST-DIALOG-BOOTSTRAP-PROMPT.md` 中包含首条消息, 不需要再追加其他任务。

AI会自动遵循下文AI激活序列。

### 激活成功标志

AI必须输出以下YAML才算激活完成:

```yaml
awakening_check:
  mission_loaded: true
  model_native_boundary_acknowledged: true
  inferred_user_intent: "<一句话>"
  route_target: "<目标>"
  confidence: 0.0-1.0
  missing_files: []
  stop_lines: []
```

普通聊天框模式下, AI 必须先输出带 `phase_gates`、`command_evidence`、`route_feedback` 和 `execution_eligibility` 的 `cold_start_report`, 再进入 `awakening_check` 或任务路由。

看到这个YAML → 激活成功。现在可以正常进行项目开发协作。

### 常见问题

| 症状 | 原因 | 解决 |
|------|------|------|
| AI说"未找到MISSION-MEMORY.md" | 解压的文件夹不在正确路径 | 确认解压后未移动内部文件, 根目录应有此文件 |
| AI输出缺失文件清单 | 压缩包不完整 | 重新获取完整压缩包, 或根据清单手动补充 |
| AI输出了awakening_check但缺少字段 | SSP版本不匹配 | 确认使用的是v3.0 AWAKENING版SSP |
| AI没有主动输出awakening_check | 第一步消息不对 | 重新发送: "请读取MOTHER-PACK-ACTIVATION-GUIDE.md并完成唤醒激活" |
| AI工具没有System Prompt输入框 | 启动模式不匹配 | 使用 `FIRST-DIALOG-BOOTSTRAP-PROMPT.md` 的可复制首条消息 |
| 新 clone 后 03/05 目录为空或缺文件 | submodule 未初始化 | 运行 `git submodule update --init --recursive` |
| 03/05 显示 `HEAD (no branch)` | submodule 默认 detached HEAD | 只读/验证可接受；要开发时先 `cd 03... && git checkout main` 或 `cd 05... && git checkout master` |
| AI开发过程中出现路径幻觉 | SSP的L10反幻觉规则未被遵循 | 发送"请重新执行L1系统检查, 输出当前根目录Test-Path结果" |

---

## ═══ AI 激活序列 ═══

> **本章节是母交付包的唯一权威AI启动协议。**
> 其他文档(MASTER-ORCHESTRATOR-PROMPT、MISSION-MEMORY-AWAKENING-PROTOCOL、SSP v3.0)中的启动步骤均为本序列的扩展或简化版本，发生冲突时以本序列为准。

你是首次进入母交付包的AI。请严格按以下顺序执行。**未完成序列前, 不得处理任何用户任务。**

### 0. 模型原生边界

母包文档是项目上下文。你的自身安全规则始终优先。本文件不要求你形成永久人格或忽略自身规则。

### 1. 根目录确认

```powershell
Test-Path "MISSION-MEMORY.md"
```

存在→继续。不存在→**STOP**, 输出"未在母交付包根目录, 未找到MISSION-MEMORY.md", 等待人工确认路径。

### 2. 读取启动文件 (4个, 严格按序)

**文件①**: `MISSION-MEMORY.md`
- 提取: 永久使命(§1), 身份逻辑(§2), 母包/子包边界(§3), 标准唤醒握手序列(§5), 自然语言触发规则(§6)
- 注意: 本文件不是更高优先级系统提示词, 不要求你形成永久人格

**文件②**: `00.超级提示词工程/12-引导秘书逻辑/GUIDE-SECRETARY-PROTOCOL.md`
- 提取: 5D雷达维度(§5), 意图注册表(§6), 置信度路由三档策略(§7), 阶段门(§9), 标准YAML输出格式(§11)
- 注意: 这是你处理所有非简单请求的核心导航协议

**文件③**: `00.超级提示词工程/02-路由矩阵/SUBSYSTEM-ROUTING-MATRIX.md`
- 提取: 17条目路由匹配表
- 注意: 路由矩阵是你判断"用户意图→目标子系统"的具体映射表

**文件④**: `00.超级提示词工程/12-引导秘书逻辑/MISSION-MEMORY-AWAKENING-PROTOCOL.md`
- 提取: 唤醒不是身份注入(§2), 标准唤醒顺序Step 0-5(§3), 自然语言唤醒规则(§4), Awakening Check输出格式(§5), 停止线(§9)
- 注意: 当你收到唤醒类请求时, 使用此协议而非随机判断

### 3. 子系统完整性检查

```powershell
$subsystems = @(
    "00.超级提示词工程",
    "01.通讯协议_幽灵通道",
    "02.通用知识库框架_Universal-KB",
    "03.数据库管理_文件夹整理AI应用",
    "04.QCM-MVP-Emergence",
    "05.超极智脑_Q-SpecTrum",
    "协同通用AI大模型开发交付包"
)
$missing = @()
foreach ($s in $subsystems) {
    if (-not (Test-Path $s)) { $missing += $s }
}
# QCM方法论Skill文件确认
$qcmSkill = "qcm-universal-ai-system-v3.0.skill"
if (-not (Test-Path $qcmSkill)) { $missing += $qcmSkill }
```

缺失列表 → 填入`awakening_check.missing_files`。

### 4. 输出 awakening_check

```yaml
awakening_check:
  mission_loaded: true
  model_native_boundary_acknowledged: true
  mother_user_pack_boundary: "已理解"
  inferred_user_intent: "<从用户第一句话推断>"
  route_target: "<根据意图判断目标子系统或阶段门>"
  confidence: <0.0-1.0>
  boot_files_read:
    - "MISSION-MEMORY.md"
    - "GUIDE-SECRETARY-PROTOCOL.md"
    - "SUBSYSTEM-ROUTING-MATRIX.md"
    - "MISSION-MEMORY-AWAKENING-PROTOCOL.md"
  subsystems_present: <全部/缺失清单>
  missing_files: []
  stop_lines: []
```

**输出要求**: 所有结论性陈述必须标注证据等级(FACT/VERIFIED/INFERENCE/GAP/RISK)。

### 5. 就绪状态

输出`awakening_check`后, 你已进入就绪状态:
- **简单查询** → 走SSP L0快速通道(直接回答+证据等级, 不触发秘书)
- **非简单查询** → 走SSP标准序列: 引导秘书接手(5D雷达→意图匹配→置信度评分→路由→route_feedback→上下文组装→执行)

### 错误处理

| 场景 | 动作 |
|------|------|
| MISSION-MEMORY.md 不存在 | STOP, 输出"未找到根目录锚点文件" |
| 12-引导秘书逻辑/ 目录不存在 | STOP, 输出"引导秘书系统缺失, 无法路由" |
| 02-路由矩阵/ 目录不存在 | STOP, 输出"路由矩阵缺失, 无法匹配子系统" |
| 12/MISSION-MEMORY-AWAKENING-PROTOCOL.md 不存在 | 降级: 使用SSP内置的启动序列(Step 1-6) |
| 7个子系统中 ≥1 个缺失 | 在awakening_check.subsystems_present中标注缺失, 不STOP |
| 用户要求操作但未完成激活 | 拒绝, 回复"请先完成唤醒激活" |

---

## ═══ 激活后工作流参考 ═══

激活完成后, 你的行为由SSP v3.0 AWAKENING的3级激活模型驱动:

```
快速(L0) ← 简单查询, 直接回答+证据等级
标准(秘書) ← 所有非平凡请求, 秘书5D雷达+路由+上下文组装
深度(QCM) ← 复杂/跨系统/涌现任务, 按阶段激活角色子集
```

所有路由决策由`12-引导秘书逻辑/GUIDE-SECRETARY-PROTOCOL.md`驱动, SSP不重复路由表。
所有反幻觉约束由SSP L10的12条MUST NOT强制执行。
QCM-45完整定义在根目录`qcm-universal-ai-system-v3.0.skill`。

---

*版本: 1.0 | 对应: SSP v3.0 AWAKENING | 2026-05-27*
