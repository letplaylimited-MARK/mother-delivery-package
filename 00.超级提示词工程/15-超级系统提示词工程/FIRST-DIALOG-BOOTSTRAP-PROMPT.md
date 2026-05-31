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

## 可复制首条消息

```text
你正在接手一个面向通用 AI 协同开发的母包仓库:

https://github.com/letplaylimited-MARK/mother-delivery-package

请先不要重构、不要扩写愿景、不要假装已经完整读取。你的第一目标是完成“冷启动接手验证”: 下载完整仓库、初始化 submodule、读取权威入口、运行验证、输出可复盘的启动报告, 然后再根据我的具体任务路由到子系统。

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
python qa_runner.py validate
python qa_runner.py status
python qa_runner.py consistency

首次输出必须包含以下 YAML, 字段不可省略:

cold_start_report:
  repo_root_confirmed: true|false
  clone_mode: "fresh_clone|existing_checkout|not_available"
  submodules_ready: true|false
  submodule_branch_state: "detached_clean|on_branch|not_checked|not_available"
  boot_files_read:
    - "<实际读取文件>"
  validation:
    qa_validate: "PASS|FAIL|NOT_RUN"
    qa_status: "PASS|FAIL|NOT_RUN"
    qa_consistency: "PASS|FAIL|NOT_RUN"
  inferred_user_intent: "<从我首条消息推断>"
  route_target: "<00|01|02|03|04|05|USER_PACK|ROOT|UNKNOWN>"
  confidence: 0.0-1.0
  route_feedback:
    selected_route: "<选择原因>"
    rejected_routes:
      - "<未选择原因>"
    needed_context:
      - "<下一步最小必读文件>"
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

执行约束:
1. route_feedback 输出前, 不要开始写文件。
2. 缺少 requirement/specification/task_boundary/verification_anchor 任意一项时, 先澄清或建立最小规格。
3. 复杂跨系统任务先做计划和验证门, 再编辑。
4. 每次编辑后必须运行相关验证; 不能运行时要把原因标为 GAP。
5. 只修复与当前任务、失败验证、过期权威文档或具体交付阻塞相关的问题。
6. 不要为了“更完善”无限扩写; 以可运行、可验证、可交接为完成标准。
7. 如果只是阅读、路由或验证, submodule detached HEAD 可接受; 如果要编辑 03/05, detached HEAD 是停止线, 必须先切换到对应分支。

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
