# V1 → V2 迁移指引

## 概述

本母交付包中存在两个名称相近但定位完全不同的知识管理项目：

| 属性 | V1: Universal-KB | V2: 数据库管理应用 |
|------|-------------------|-------------------|
| **路径** | `02.通用知识库框架_Universal-KB/` | `03.数据库管理_文件夹整理AI应用/` |
| **定位** | 轻量级**模板** | 完整可运行**应用** |
| **可运行** | 否（纯目录结构 + 概念代码） | 是（Flask Web + MCP Server） |
| **文件数** | ~21 | ~172 |
| **核心能力** | 目录范式、MemoryOS 概念引擎、AGENTS 配置 | 文件整理、向量检索、MCP 工具、AI 协作 |
| **技术栈** | 纯 Markdown + Python 概念脚本 | Flask + FAISS + SQLite + MCP |
| **适用场景** | 理解知识管理设计理念 | 实际项目知识管理 |

## 关键差异

### V1 提供什么
- 6 层目录结构范式（raw → processed → wiki → memory → agents → output）
- MemoryOS 三层记忆引擎概念（短期 FIFO 7 条、中期热度 1000 条、长期持久 100 条）
- AGENTS.md 中的 Ingest/Query/Lint 三种工作流配置
- 知识图谱索引（concepts/entities/sources/comparisons）

### V2 在 V1 基础上新增
- **Flask Web/REST 服务**（端口 5000，`app.py`）
- **MCP Server**（20 个工具：search_all、vector_search 等，`mcp_server.py`）
- **FAISS 向量检索**（语义搜索能力）
- **24 个自动化脚本**（搜索、向量、自动整理、收件箱、工作流等）
- **完整测试套件**（103 个 pytest 测试）
- **文件夹自动整理**（AutoOrganizer）
- **多格式支持**（Markdown、PDF、代码文件）
- **Web 浏览界面**（browse/search 模板）

## 目录映射

| V1 目录 | V2 对应 | 说明 |
|---------|---------|------|
| `01-raw/` | `01-收件箱/` | 新知识入口 |
| `02-processed/` | `05-知识沉淀/` | 处理后知识 |
| `03-wiki/` | `05-知识沉淀/wiki/` | 知识图谱 |
| `04-memory/` | `.workbuddy/记忆层/` | 记忆引擎 |
| `05-agents/` | `.workbuddy/AI协作体系/` | AI 协作配置 |
| `06-output/` | `04-输出成果/` | 输出成果 |

## 迁移步骤

1. **备份 V1 数据**：将 V1 的 `03-wiki/` 和 `04-memory/` 内容复制到安全位置
2. **安装 V2 依赖**：在 V2 目录运行 `pip install -r requirements.txt`
3. **初始化 V2**：运行 `00-快速开始/setup.bat`
4. **迁移知识图谱**：将 V1 的 wiki 内容复制到 V2 的 `05-知识沉淀/wiki/`
5. **迁移记忆数据**：将 V1 的 `04-memory/long_term/` 内容放入 V2 的 `.workbuddy/记忆层/`
6. **验证**：运行 `python verify_install.py` 确认 V2 安装完整
7. **启动**：运行 `python app.py` 启动 V2 服务

## 注意事项

- V1 的 `memoryos.py` 是概念引擎，V2 使用不同的记忆实现（基于 SQLite + FAISS）
- V2 的 AGENTS 体系在 `.workbuddy/AI协作体系/` 下，与 V1 的 `AGENTS.md` 格式不同
- V1 适合作为设计参考和教学材料，不建议在生产环境使用
