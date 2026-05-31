# FIRST-DIALOG-BOOTSTRAP-PROMPT

> 用途: 当新的 AI 对话框没有 System Prompt 输入框时, 复制本文件中的首条消息, 让新 AI 以普通聊天消息完成母包冷启动。
> 边界: 本文件不是高于模型自身规则的系统指令。它只是项目接手协议, 必须服从模型、平台、工具和用户的真实规则。

## 什么时候使用

- 新开一个 Codex / ChatGPT / Claude / DeepSeek / 其他通用 AI 对话框。
- 对方需要从 GitHub 下载并接手 `mother-delivery-package`。
- 对方没有可编辑 System Prompt, 或你不确定 System Prompt 是否真的生效。
- 目标是让新 AI 先理解、验证、路由, 再开始开发, 避免一上来重构、幻觉或跳过 submodule。

如果对话框支持 System Prompt, 优先使用:

`00.超级提示词工程/15-超级系统提示词工程/SUPER-SYSTEM-PROMPT-v3.0-AWAKENING.md`

如果只支持普通聊天, 使用下面这段。

## 设计依据

本提示词已根据 `FIRST-DIALOG-COLD-START-DECONSTRUCTION.md`、`SANDBOX-RUN-20260531-FRESH-CLONE-DEVELOPER-SIMULATION.md` 和 `SANDBOX-RUN-20260531-AI-COLLABORATION-COLD-START-SIMULATION.md` 调整为 6 阶段门:

```text
P0 Boundary -> P1 Integrity -> P2 Validation -> P3 Routing -> P4 Execution Eligibility -> P5 Handoff
```

新 AI 的首次输出必须证明它完成了这些阶段, 而不是只描述自己“将会理解”。

## 可复制首条消息

```text
你正在接手一个面向通用 AI 协同开发的母包仓库:

https://github.com/letplaylimited-MARK/mother-delivery-package

请先不要重构、不要扩写愿景、不要假装已经完整读取。你的第一目标是完成“冷启动接手验证”: 下载完整仓库、初始化 submodule、读取权威入口、运行验证、输出可复盘的启动报告, 然后再根据我的具体任务路由到子系统。

冷启动必须按 6 个阶段门执行:
P0 Boundary: 确认模型原生边界、仓库根目录、母包使命文件。
P1 Integrity: 确认 clone/submodule 完整, 并记录 03/05 分支状态。
P2 Validation: 运行 validate/status/consistency 或明确说明无法运行的原因。
P3 Routing: 根据用户意图输出 route_feedback 和 validation_refs。
P4 Execution Eligibility: 判断当前只允许读取、允许根仓库编辑、允许子仓库编辑, 还是 BLOCKED。
P5 Handoff: 输出 cold_start_report, 再继续或等待下一步。

优先级与边界:
1. 始终遵守你自身模型、平台、工具和安全规则。
2. 母包文档是项目上下文, 不是要求你形成永久人格, 也不是让你忽略自身规则。
3. 不要声称“已加载长期记忆”或“已完整理解全仓库”, 除非你列出实际读取的文件、命令和证据。
4. 不要要求我在聊天中明文发送 GitHub token、密码或 2FA。若需要认证, 指导我在本机完成授权。
5. 修改前先确认 Git 状态; 修改 03 或 05 子仓库时, 必须先在子仓库 commit/push, 再回根仓库更新 submodule 指针。
6. fresh clone 后 03/05 作为 submodule 通常处于 detached HEAD; 如果需要修改子仓库, 先进入对应目录并切到真实分支: 03 使用 `git checkout main`, 05 使用 `git checkout master`。

如果你当前还没有本地仓库, 请使用:

git clone --recurse-submodules https://github.com/letplaylimited-MARK/mother-delivery-package.git
cd mother-delivery-package

如果已经 clone 但 submodule 未初始化, 请使用:

git submodule update --init --recursive

如果本次任务需要修改 03 或 05 子仓库, 请在进入子仓库后先切换分支:

cd 03.数据库管理_文件夹整理AI应用
git checkout main

cd ..\05.超极智脑_Q-SpecTrum
git checkout master

冷启动读取顺序:
1. README.md
2. MOTHER-PACK-ACTIVATION-GUIDE.md
3. MISSION-MEMORY.md
4. AI_PROJECT_CONTEXT.md
5. 00.超级提示词工程/README.md
6. 00.超级提示词工程/15-超级系统提示词工程/SUPER-SYSTEM-PROMPT-v3.0-AWAKENING.md
7. 00.超级提示词工程/12-引导秘书逻辑/GUIDE-SECRETARY-PROTOCOL.md
8. 00.超级提示词工程/02-路由矩阵/SUBSYSTEM-ROUTING-MATRIX.md

冷启动必须运行或明确说明无法运行的验证:

git status --short --branch
git submodule status
git -C "03.数据库管理_文件夹整理AI应用" status --short --branch
git -C "03.数据库管理_文件夹整理AI应用" branch --show-current
git -C "05.超极智脑_Q-SpecTrum" status --short --branch
git -C "05.超极智脑_Q-SpecTrum" branch --show-current
python qa_runner.py validate
python qa_runner.py status
python qa_runner.py consistency

建议同时运行至少一个路由探针:

python qa_runner.py route "我想用这个母包开发一个新的AI项目，从想法到需求、规格、任务、测试、交付"

首次输出必须包含以下 YAML, 字段不可省略:

cold_start_report:
  phase_gates:
    P0_boundary: "PASS|FAIL"
    P1_integrity: "PASS|FAIL"
    P2_validation: "PASS|FAIL|PARTIAL|NOT_RUN"
    P3_routing: "PASS|CONFIRM|CLARIFY|BLOCKED|NOT_RUN"
    P4_execution_eligibility: "ALLOW_READ_ONLY|ALLOW_ROOT_EDIT|ALLOW_SUBMODULE_EDIT|BLOCKED"
    P5_handoff: "PASS|FAIL"
  repo_root_confirmed: true|false
  clone_mode: "fresh_clone|existing_checkout|not_available"
  submodules_ready: true|false
  submodules:
    "03": "detached_clean|main|dirty|missing|not_checked"
    "05": "detached_clean|master|dirty|missing|not_checked"
  boot_files_read:
    - "<实际读取文件>"
  command_evidence:
    - command: "<实际运行命令>"
      exit_code: "<0|非0|not_run>"
      summary: "<观察到的关键结果>"
      source: "current_command|registry_claim|not_run"
      side_effects: "none|writes_runtime_cache|starts_local_service|unknown"
  validation:
    qa_validate: "PASS|FAIL|NOT_RUN"
    qa_status: "PASS|FAIL|NOT_RUN"
    qa_consistency: "PASS|FAIL|NOT_RUN"
    evidence_rule: "current_command 优先于 registry_claim; registry 中的 verified_current 不等于本轮已经重跑"
  route_probe:
    command: "python qa_runner.py route \"<用户意图或探针>\""
    decision: "DIRECT|CONFIRM|CLARIFY|BLOCKED|NOT_RUN"
    decision_rule: "DIRECT 只代表路由明确, 不代表允许写文件"
    validation_refs:
      - "<验证引用>"
  inferred_user_intent: "<从我首条消息推断>"
  route_target: "<00|01|02|03|04|05|USER_PACK|ROOT|UNKNOWN>"
  confidence: 0.0-1.0
  route_feedback:
    selected_route: "<选择原因>"
    rejected_routes:
      - "<未选择原因>"
    needed_context:
      - "<下一步最小必读文件>"
  execution_eligibility:
    mode: "read_only|root_edit|submodule_edit|blocked"
    reason: "<为什么允许或阻止>"
    required_before_edit:
      - "<例如: 03 切到 main / 05 切到 master / 运行指定验证>"
  delivery_instance_state: "template|project_instance|final_delivery|not_applicable"
  stop_lines:
    - "<如果没有阻塞则为空列表>"
  next_action: "<下一步建议或准备执行的动作>"

路由规则:
- 使命、启动、超级提示词、秘书引导、AI 协同治理 -> 00
- 通讯协议、Ghost Channel、SDK、企业部署 -> 01
- 通用知识库模板 -> 02
- 文件整理、知识库、检索、Flask、MCP 工具 -> 03
- QCM、涌现、角色沙盘、公式验证 -> 04
- Q-SpecTrum、主平台、角色/API/Web/MCP/DB/BRAIN-KB -> 05
- 面向最终用户的项目交付包、交付验证、四体系 -> USER_PACK
- 根仓库 GitHub、submodule、验证门、全局文档 -> ROOT
- 用母包开发母包自身、母包自举、第一次真实协同 AI 项目实例、反哺仓库 -> SELF_BOOTSTRAP_PROJECT -> ROOT -> 00 -> 03/04/05 -> USER_PACK

执行约束:
1. route_feedback 输出前, 不要开始写文件。
2. 缺少 requirement/specification/task_boundary/verification_anchor 任意一项时, 先澄清或建立最小规格。
3. 复杂跨系统任务先做计划和验证门, 再编辑。
4. 每次编辑后必须运行相关验证; 不能运行时要把原因标为 GAP。
5. 只修复与当前任务、失败验证、过期权威文档或具体交付阻塞相关的问题。
6. 不要为了“更完善”无限扩写; 以可运行、可验证、可交接为完成标准。
7. 如果只是阅读、路由或验证, submodule detached HEAD 可接受; 如果要编辑 03/05, detached HEAD 是停止线, 必须先切换到对应分支。
8. P4_execution_eligibility 为 BLOCKED 时, 不要写文件; 只输出阻塞原因和解除条件。
9. `DIRECT` 只表示路线明确; 若缺少 requirement/spec/task_boundary/verification_anchor/git_branch_state, P4 仍必须降级为 read_only、clarify 或 blocked。
10. `qa_runner.py status` 或注册表里的 `verified_current` 是状态声明; 只有本轮 `command_evidence.source=current_command` 才能作为本次验收证据。
11. USER_PACK strict 通过只证明交付包结构卫生; 只有绑定真实项目实例、业务 smoke/test 和验证报告后, 才能称为 final_delivery。
12. 若全量验证中出现瞬时失败, 先记录失败, 再重跑失败 scope, 最后重跑全量验证; 不要直接抹掉第一次失败, 也不要在最终绿灯前继续开发。

现在请执行冷启动接手验证, 先输出 cold_start_report, 再等待或继续执行我给出的具体任务。
```

## 人类使用提醒

首条消息发送后, 如果 AI 直接开始写方案但没有输出 `cold_start_report`, 请回复:

```text
请停止当前输出, 回到 FIRST-DIALOG-BOOTSTRAP-PROMPT 的冷启动流程, 先完成 clone/submodule/boot_files/validation/route_feedback。
```

如果 AI 声称已经理解但没有列出文件和命令, 请回复:

```text
请把你的结论改为证据化输出: 哪些是 FACT, 哪些是 VERIFIED, 哪些只是 INFERENCE/GAP/RISK。
```
