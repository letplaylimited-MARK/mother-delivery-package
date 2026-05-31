# AI Project Context

> 用途：交付给最终用户的项目上下文文档（母交付包 AI_PROJECT_CONTEXT.md 的精简版）。
> 生成时间：2026-05-31。

## 项目概述

本项目是一个 AI 协同开发交付包，帮助开发者与通用 AI 大模型长期、稳定、可验证地协同开发项目。核心能力包括结构化需求锻造（SpecForge）、多角色协同评估（QCM）、多智能体通信协议（Ghost Channel）、知识库管理（MCP）、统一调度平台（Q-SpecTrum）和全链路验证体系。

## 项目统计

| 项 | 数值 |
|---|---|
| 子系统 | 7 个目录子系统（00-05 + 协同交付包）+ 1 个 QCM `.skill` 能力包 |
| 文件总数 | 当前审计快照 1150；权威值以 `00.超级提示词工程/14-全链路审计与运行对齐/ATOMIC-FILE-INVENTORY-SUMMARY.md` 为准 |
| 验证注册 | 31 项（31 项自动验证；0 项 manual/current） |
| 测试证据 | 01 SDK 184、03 知识库 107、04 QCM 25+38+6、QCM Skill 173、05 Q-SpecTrum 158 pytest + 13 E2E |
| Git 仓库 | GitHub: letplaylimited-MARK/mother-delivery-package；当前工作树状态以 `git status` 为准 |
| Python 包依赖 | 各子系统使用自己的 `requirements.txt` / `pyproject.toml`；当前最低交接口径为 Python 3.10+ |

## 核心验证结果（2026-05-31）

```
AUTO PASS: 31/31
MANUAL/CURRENT: 0
FAIL/WARN/SKIP: 0
Consistency: 10/10 PASS
```

## 子系统快速索引

| 子系统 | 一句话定位 | 入口命令 |
|---|---|---|
| 00 超级提示词工程 | 控制平面：启动/路由/阶段门/审计 | 00/README.md |
| 01 幽灵通道 | 通信协议 + SDK | VERIFY.ps1 |
| 02 通用知识库 | 知识管理模板 | 04-memory/memoryos.py |
| 03 数据库管理 | 知识库应用（Flask+MCP） | verify_install.py + pytest tests -q |
| 04 QCM-MVP | 共鸣公式 + 涌现检测 | test_qcm_all.py |
| 05 Q-SpecTrum | 主平台（15 角色 + Web + API + MCP） | verify-integration.py + run.py --e2e |
