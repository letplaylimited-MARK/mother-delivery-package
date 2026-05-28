# AI Project Context

> 用途：交付给最终用户的项目上下文文档（母交付包 AI_PROJECT_CONTEXT.md 的精简版）。
> 生成时间：2026-05-28。

## 项目概述

本项目是一个 AI 协同开发交付包，帮助开发者与通用 AI 大模型长期、稳定、可验证地协同开发项目。核心能力包括结构化需求锻造（SpecForge）、多角色协同评估（QCM）、多智能体通信协议（Ghost Channel）、知识库管理（MCP）、统一调度平台（Q-SpecTrum）和全链路验证体系。

## 项目统计

| 项 | 数值 |
|---|---|
| 子系统 | 7 个（00-05 + 协同交付包） |
| 文件总数 | ~1118 个（排除 cache） |
| 验证命令 | 18 条（qa_runner.py validate） |
| 测试用例 | 274+（103 + 25 + 38 + 18 + 31 + 其他） |
| Git 仓库 | GitHub: letplaylimited-MARK/mother-delivery-package（10 commits） |
| Python 包依赖 | 6 个核心（cryptography, Flask, numpy, chromadb, pytest, pytest-asyncio） |

## 核心验证结果（2026-05-28）

```
PASS:  12  (含 299 文件完整性、25 QCM tests、38 paper tests、18 SDK tests、31 集成验证)
FAIL:   0  (之前唯一的 FAIL 已通过)
WARN:   1  (VAL-02-TEMPLATE-REVIEW: README 夸大)
MANUAL: 4  (需人工确认的项目级检查)
```

## 子系统快速索引

| 子系统 | 一句话定位 | 入口命令 |
|---|---|---|
| 00 超级提示词工程 | 控制平面：启动/路由/阶段门/审计 | 00/README.md |
| 01 幽灵通道 | 通信协议 + SDK | VERIFY.ps1 |
| 02 通用知识库 | 知识管理模板 | 04-memory/memoryos.py |
| 03 数据库管理 | 知识库应用（Flask+MCP） | verify_install.py |
| 04 QCM-MVP | 共鸣公式 + 涌现检测 | test_qcm_all.py |
| 05 Q-SpecTrum | 主平台（15 角色 + Web + API） | verify-integration.py |
