# 协同通用AI大模型开发交付包 -- INDEX

> 定位: **四体系交付包骨架** -- 开发者完成项目后交给最终用户的装配区
> 边界: 不硬编码本机绝对路径; 由开发者按项目成果填入真实内容

## 文件结构
```
协同通用AI大模型开发交付包/
├── README.md                    本包总说明
├── 交付包组装规则.md            组装流程与质量门
├── VERIFY-DELIVERY.ps1          交付验证脚本
├── AI_PROJECT_CONTEXT.md         AI 项目上下文地图
├── HANDOFF.md                    当前交接状态与风险
├── VALIDATION_REPORT.md          当前验证证据
├── TRACEABILITY-MATRIX.md        目标/需求/任务/测试追踪
├── CHANGELOG.md                  变更历史
├── 01-价值体系/                 项目为什么有价值
├── 02-功能体系/                 项目能做什么
├── 03-结构体系/                 模块/文件/接口/依赖组成
└── 04-运作体系/                 安装/启动/验证/维护/排错
```

## 四大交付体系
| 体系 | 回答的问题 | 入口 |
|------|-----------|------|
| 价值体系 | 解决谁的什么问题, 用什么指标验收 | 01-价值体系/README.md |
| 功能体系 | 用户如何使用, AI/系统能力边界 | 02-功能体系/README.md |
| 结构体系 | 模块/文件/数据/接口/依赖组成 | 03-结构体系/README.md |
| 运作体系 | 安装/启动/验证/维护/升级/排错 | 04-运作体系/README.md |

## 关键入口
| 文件 | 用途 | 优先级 |
|------|------|--------|
| README.md | 项目用途、适用对象、交付边界 | 高 |
| AI_PROJECT_CONTEXT.md | 项目上下文地图，供其他 AI 快速接手 | 高 |
| HANDOFF.md | 当前状态、风险、后续事项 | 高 |
| VALIDATION_REPORT.md | 当前验证结果与证据 | 高 |
| TRACEABILITY-MATRIX.md | 目标/需求/任务/测试/审计映射 | 高 |
| 04-运作体系/README.md | 安装/启动/验证/排错命令 | 高 |
| VERIFY-DELIVERY.ps1 | 自动化交付验证 (普通模式 / -Strict 模式) | 高 |
| 交付包组装规则.md | 组装流程与质量门 | 中 |
| 01-价值体系/README.md | 项目价值与验收指标 | 中 |
| 02-功能体系/README.md | 功能清单与能力边界 | 中 |
| 03-结构体系/README.md | 模块组成与依赖 | 中 |

## 快速开始

验证骨架结构:
```
powershell -ExecutionPolicy Bypass -File .\VERIFY-DELIVERY.ps1
```

正式交付前严格验证:
```
powershell -ExecutionPolicy Bypass -File .\VERIFY-DELIVERY.ps1 -Strict
```

其他 AI 进入时的读取顺序:
1. README.md
2. AI_PROJECT_CONTEXT.md
3. HANDOFF.md
4. VALIDATION_REPORT.md
5. TRACEABILITY-MATRIX.md
6. CHANGELOG.md
7. 01-价值体系/README.md
8. 02-功能体系/README.md
9. 03-结构体系/README.md
10. 04-运作体系/README.md

最终用户第一步: README.md -> 04-运作体系/README.md -> 项目验证入口

## 当前状态

骨架阶段: 入口说明、组装规则、验证脚本、四大体系模板已建立。
后续每开发一个具体项目，将项目真实内容填入四个体系。
