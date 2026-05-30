# Mother Delivery Package (母交付包)

> 面向 AI 协同开发的完整生产系统交付包，包含七个子系统、验证体系与用户交付框架。

## 架构概览

本仓库采用 **Git Monorepo** 结构，根目录管理母包级文档和 `00.超级提示词工程`，`03` 和 `05` 作为 Git Submodule 引入。

| # | 子系统 | 文件数 | 说明 | GitHub |
|---|--------|--------|------|--------|
| 00 | 超级提示词工程 | 52 | 跨项目 AI 协同的提示词操作系统 | 随根仓库 |
| 01 | 通讯协议 / 幽灵通道 | 295 | Ghost Channel v1.0 协议、SDK、企业部署 | 随根仓库 |
| 02 | 通用知识库框架 (Universal-KB) | 21 | V1 知识管理模板 | 随根仓库 |
| 03 | 数据库管理 / 文件整理 AI 应用 | 172+ | V2 可运行应用 (Flask + MCP + FAISS) — submodule | [knowledge-base-manager](https://github.com/letplaylimited-MARK/knowledge-base-manager) |
| 04 | QCM-MVP-Emergence | 146 | 共鸣公式、22 公式、涌现验证 (63 tests) | 随根仓库 |
| 05 | 超极智脑 / Q-SpecTrum | 431+ | 主平台：15 角色、Web UI、API、DB、知识库 — submodule | [Q-Spectrum](https://github.com/letplaylimited-MARK/Q-Spectrum) |
| — | 协同通用 AI 大模型开发交付包 | 13 | 用户交付包骨架（价值/功能/结构/运作四体系） | 随根仓库 |

> **统计口径**：00/01/02/04/协同的文件数为 `git ls-files` 跟踪数；03/05 为独立 submodule，数字标注 `+` 表示含 submodule 内部展开，根仓库仅跟踪指针文件。根仓库总跟踪 542 文件（含 submodule 指针），全量展开约 1082 文件。

## 快速开始

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/letplaylimited-MARK/mother-delivery-package.git
cd mother-delivery-package

# 如果已经 clone 但未初始化 submodule
git submodule update --init --recursive
```

## 验证

根目录提供 `qa_runner.py` 统一验证工具（18 项验证规则，含 5 项 MANUAL）：

```bash
python qa_runner.py validate    # 运行全量验证
python qa_runner.py status      # 查看验证状态
python qa_runner.py consistency # 跨文档一致性检查
python qa_runner.py route       # 路由矩阵分析
```

用户交付包验证（需 PowerShell）：

```powershell
cd 协同通用AI大模型开发交付包
powershell -ExecutionPolicy Bypass -File .\VERIFY-DELIVERY.ps1        # 普通模式
powershell -ExecutionPolicy Bypass -File .\VERIFY-DELIVERY.ps1 -Strict # 严格模式
```

## 文件导航

### 根级文件

| 文件 | 用途 |
|------|------|
| `AI_PROJECT_CONTEXT.md` | **全局导航地图** — 目录结构、子系统说明、跨系统关系、启动命令、CI/CD、开发迭代记录 |
| `LICENSE` | MIT 开源许可证 |
| `MISSION-MEMORY.md` | 母包使命、边界、AI 唤醒锚点 |
| `MOTHER-PACK-ACTIVATION-GUIDE.md` | **唯一权威 AI 启动协议** |
| `开发者母交付包使用说明.md` | 面向 zip 包接收者的完整使用指引（交付流程、子系统定位、验证步骤） |
| `qa_runner.py` | 全量验证工具（validate / status / consistency / route） |
| `qcm-universal-ai-system-v3.0.skill` | QCM 质量评估框架（ZIP，45 角色 / 9 阶段 / 24 维） |
| `MOTHER-PACK-DEEP-ANALYSIS-REPORT-v3.0-FLYWHEEL.html` | 飞轮审计最终报告（R1 / R2 / R3 完整记录） |
| `V1_TO_V2_MIGRATION.md` | V1（模板）→ V2（可运行应用）迁移历史参考 |

### 阅读顺序

**人类开发者**：本文 → `AI_PROJECT_CONTEXT.md` → 对应子系统 README

**AI 协作者**：`MOTHER-PACK-ACTIVATION-GUIDE.md` → `MISSION-MEMORY.md` → `AI_PROJECT_CONTEXT.md` → 按任务路由进入子系统

## 技术栈

- **Python** 3.13+（验证工具、SDK、QCM 测试、平台引擎）
- **Flask**（03 知识库 Web 应用、MCP Server）
- **FAISS**（向量检索）
- **ChromaDB**（05 平台知识库）
- **SQLite**（平台数据库、搜索索引）
- **PowerShell**（交付验证脚本）
- **GitHub Actions**（CI/CD 自动验证）

## 子系统依赖关系

```
05 Q-SpecTrum (集成层)
 ├── 01 Ghost Channel (通信协议 / 同步 / 安全)
 ├── 03 Universal-KB V2 (知识库 / MCP / 文件整理)
 └── 04 QCM-MVP (共鸣公式 / 角色协同 / 涌现检测)

00 超级提示词工程 (方法论层 — 服务于所有子系统)
```

## 许可证

[MIT License](LICENSE)
