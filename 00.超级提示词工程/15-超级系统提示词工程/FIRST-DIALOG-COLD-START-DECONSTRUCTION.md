# First Dialog Cold Start Deconstruction

> 用途: 把 2026-05-31 fresh clone 开发者模拟反向拆解成首次对话启动协议的设计依据。  
> 范围: `FIRST-DIALOG-BOOTSTRAP-PROMPT.md`, `MOTHER-PACK-ACTIVATION-GUIDE.md`, ROOT 验证门, 03/05 submodule 开发边界。  
> 状态: VERIFIED from fresh GitHub clone simulation.

## 1. 模拟证明了什么

这次模拟不是证明“当前本机能跑”, 而是证明一个新的开发者或新的 AI 对话框可以只依赖 GitHub 仓库完成接手:

```yaml
simulation_result:
  clone_source: "https://github.com/letplaylimited-MARK/mother-delivery-package"
  clone_mode: "git clone --recurse-submodules"
  root_validation: "31/31 PASS"
  status: "PASS exit=0"
  consistency: "10/10 PASS"
  route_probe_count: 4
  route_feedback_present: true
  workspace_clean_after_validation: true
  main_friction: "03/05 submodules are detached HEAD after fresh clone"
```

## 2. 冷启动的真实阶段

首次对话不能只要求 AI “读取仓库”。它必须把冷启动拆成 6 个阶段门:

| 阶段 | 目标 | 必须证据 | 不通过时 |
|---|---|---|---|
| P0 Boundary | 确认模型原生边界与仓库根目录 | `MISSION-MEMORY.md` 存在, 说明不覆盖模型规则 | STOP |
| P1 Integrity | 确认 clone/submodule 完整 | `git status`, `git submodule status` | 修 clone/submodule, 不进入任务 |
| P2 Validation | 证明当前仓库可运行 | `qa_runner.py validate/status/consistency` | 标记 FAIL/GAP, 不写文件 |
| P3 Routing | 把用户语言路由到子系统 | `route_feedback`, `validation_refs` | CLARIFY/CONFIRM |
| P4 Execution Eligibility | 判断是否允许编辑 | root clean, branch state, required IDs, validation anchor | BLOCKED or ask |
| P5 Handoff | 输出可复盘启动报告 | `cold_start_report` + next action | 缺字段则重跑 |

## 3. 首条提示词必须防止的 5 类失败

```yaml
failure_modes:
  shallow_confidence:
    symptom: "AI 说已经完整理解, 但没有列出读取文件和命令"
    guardrail: "cold_start_report.boot_files_read + command_evidence"
  submodule_incomplete:
    symptom: "03/05 目录为空或文件不完整"
    guardrail: "git clone --recurse-submodules + git submodule status"
  detached_head_editing:
    symptom: "AI 在 03/05 detached HEAD 上提交修改"
    guardrail: "submodule_branch_state + edit requires 03 main / 05 master"
  route_without_feedback:
    symptom: "AI 直接执行, 没有 selected_route/rejected_routes/validation_refs"
    guardrail: "route_feedback is mandatory before writing"
  endless_expansion:
    symptom: "继续创建提示词/角色/集成层, 但没有失败验证或真实需求"
    guardrail: "stop unless validation fails, authority doc drifts, or handoff blocker exists"
```

## 4. 最佳首次对话结构

首次消息应要求 AI 先输出一份机器可读报告, 而不是先输出解释:

```yaml
cold_start_report:
  phase_gates:
    P0_boundary: "PASS|FAIL"
    P1_integrity: "PASS|FAIL"
    P2_validation: "PASS|FAIL|PARTIAL"
    P3_routing: "PASS|CONFIRM|CLARIFY|BLOCKED"
    P4_execution_eligibility: "ALLOW_READ_ONLY|ALLOW_ROOT_EDIT|ALLOW_SUBMODULE_EDIT|BLOCKED"
  command_evidence:
    - command: "<exact command>"
      exit_code: 0
      summary: "<short observed result>"
  submodules:
    "03": "detached_clean|main|dirty|missing"
    "05": "detached_clean|master|dirty|missing"
  route_feedback:
    selected_route: "<route>"
    rejected_routes: []
    validation_refs: []
  stop_lines: []
```

This makes the first message useful for both humans and future AI models.

## 5. What Should Not Be Added

The simulation did not justify adding another orchestration layer, another permanent role system, or another broad refactor. It only justified:

- making the cold-start report more explicit
- requiring command evidence
- recording submodule branch state
- making execution eligibility explicit
- preserving the stop rule

## 6. Prompt Improvement Decision

```yaml
decision:
  update_target: "FIRST-DIALOG-BOOTSTRAP-PROMPT.md"
  add_fields:
    - "phase_gates"
    - "command_evidence"
    - "submodules"
    - "execution_eligibility"
    - "route_probe"
  preserve:
    - "model-native boundary"
    - "token secrecy"
    - "submodule branch switch rule"
    - "route_feedback before writes"
    - "no endless expansion"
  validation_after_change:
    - "python qa_runner.py validate --scope ROOT"
    - "python qa_runner.py validate --scope P00_SUPER_PROMPT"
    - "python qa_runner.py consistency"
```
