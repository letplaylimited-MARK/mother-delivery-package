# Schemas

这里存放从《幽灵通道协议规范稿 / SDK 草案》真正导出的 JSON Schema 文件。

## 已导出文件

| 文件 | 作用 |
|------|------|
| `delta-payload.schema.json` | 差分载荷对象 |
| `encrypted-stream.schema.json` | 线协议主消息对象 |
| `ack-message.schema.json` | 回执确认对象 |
| `sync-result.schema.json` | SDK 同步结果对象 |
| `error-object.schema.json` | 标准错误对象 |
| `vector-clock.schema.json` | 因果顺序向量时钟对象 |
| `audit-entry.schema.json` | 审计追踪对象 |
| `workflow-step.schema.json` | 工作流步骤状态对象 |
| `snapshot-record.schema.json` | 快照记录对象 |

## 建议用法

1. 在 Python / TypeScript SDK 中作为运行时校验依据
2. 在协议测试中做 conformance 校验
3. 在 AI 执行层做对象约束验证

## 下一步可继续导出
