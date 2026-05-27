# AI Context Pack Template

> 用途：每次让 AI 处理任务前，先把必要上下文压缩成一个可复用上下文包。  
> 原则：少而准，能验证，可交接。

## 模板

```text
# AI Context Pack

## 0. 引导秘书判断
- 原始意图:
- 规范化意图:
- Intent ID:
- Route Decision: DIRECT / CONFIRM / CLARIFY / BLOCKED
- Confidence:
- USO ID:
- Ledger Ref: 00.超级提示词工程/14-全链路审计与运行对齐/UNIFIED-STATUS-LEDGER.yaml
- Validation Refs:
- 5D Radar:
  - Track:
  - Platform:
  - People:
  - Style:
  - Supplement:
- Route Feedback:
  - Selected Route:
  - Rejected Routes:
  - Confidence After Routing:
  - Feedback To Guide: keep / confirm / clarify / block / reroute
  - Blocked Reason:
- 交接包: 有 / 无 / 待生成

## 1. 任务
- 用户目标:
- 任务类型: 开发 / 文档 / 验证 / 架构 / 集成 / 研究
- 优先级:
- 关联 ID: GOAL- / REQ- / PRD- / SPEC- / TASK-
- 当前阶段: INBOX / CLARIFIED / PRD_READY / SPEC_READY / PLANNED / IN_PROGRESS / PAUSED / BLOCKED / VERIFIED / REVIEWED / RELEASED / CRYSTALLIZED / SUPERSEDED
- 暂停/阻塞/替代原因:
- 恢复条件:

## 2. 子系统
- 主子系统:
- 辅助子系统:
- 不应触碰的目录:

## 2.1 五个锚点
- 需求锚点: 用户目标 / 问题 / 非目标 / 验收指标
- 规格锚点: 已确认的接口 / 功能 / 约束 / 测试标准
- 任务锚点: 当前任务 / 阻塞项 / 依赖 / WIP 限制 / 下一步
- 记忆锚点: 需要读取和写回的 HANDOFF / MEMORY / 知识图谱位置
- 验证锚点: 允许运行的命令 / 预期结果 / 失败降级方式

## 3. 必读文件
- 全局:
  - AI_PROJECT_CONTEXT.md
  - 00.超级提示词工程/README.md
- 子系统:
  - ...

## 4. 当前已知事实
- E1 已读文件事实:
- E2 已运行命令事实:
- E3 已测试/审计事实:
- E0 推断或未验证:

## 5. 运行入口
- 命令 1:
- 命令 2:

## 6. 验证标准
- 验证命令:
- 预期结果:
- 如果失败:

## 7. 输出格式
- 需要修改文件:
- 需要生成文档:
- 需要交接摘要:

## 8. 风险
- 文档漂移:
- 旧副本:
- 编码/路径:
- 依赖/环境:

## 9. 交接与沉淀
- 需要更新的 PRD/SPEC/TASK/TEST:
- 需要写入的 ADR/MEM:
- 需要更新的用户交付包四体系:
- 下一位 AI 接手时先读:
```

## 示例：平台开发任务

```text
主子系统: 05.超极智脑_Q-SpecTrum
必读:
  - AI_PROJECT_CONTEXT.md
  - 05.超极智脑_Q-SpecTrum/INDEX.md
  - 05.超极智脑_Q-SpecTrum/AGENTS.md
  - 05.超极智脑_Q-SpecTrum/智腦協議-BRAIN-PROTOCOL.md
验证:
  - python verify-integration.py
  - $env:PYTHONUTF8='1'; python run.py --status
风险:
  - 默认 PowerShell GBK 可能无法打印 emoji
  - requirements.txt 与 pyproject.toml 依赖说明不一致
锚点:
  - 任务锚点: 当前只处理一个 TASK，不接受顺手重构
  - 验证锚点: verify-integration.py + run.py --status
```

## 示例：知识库/MCP 任务

```text
主子系统: 03.数据库管理_文件夹整理AI应用
必读:
  - 03.数据库管理_文件夹整理AI应用/AGENTS.md
  - 03.数据库管理_文件夹整理AI应用/mcp_server.py
验证:
  - python verify_install.py
  - pytest tests/ -v
风险:
  - 未配置 .env 只影响高级 AI 调用
```

## 示例：协议 SDK 任务

```text
主子系统: 01.通讯协议_幽灵通道
必读:
  - 01.通讯协议_幽灵通道/00_总览/PROJECT_HANDOFF.md
  - 01.通讯协议_幽灵通道/03_SDK与集成/README.md
验证:
  - powershell -ExecutionPolicy Bypass -File .\VERIFY.ps1
风险:
  - 有旧审计报告残留，不要只看单份报告判断当前状态
```
