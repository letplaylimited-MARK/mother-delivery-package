# Universal-KB 通用知识库框架 V1.0 [模板]

> **版本**: V1.0
> **创建时间**: 2026-04-21
> **定位**: 轻量级知识管理**模板**（非可运行应用）。提供目录结构、MemoryOS 概念引擎和 AGENTS 配置参考。
>
> **V2 可运行版**: 位于 `../03.数据库管理_文件夹整理AI应用/`，基于 Flask + MCP + 向量检索的完整知识管理应用。
> **迁移指引**: 参见根目录 `V1_TO_V2_MIGRATION.md`

---

## 🎯 核心特性

- **通用设计**: 无业务依赖，可用于任何领域
- **三层架构**: 原始 → 知识图谱 → 长期记忆
- **完整功能**: Ingest/Query/Lint 全套工作流
- **开箱即用**: AGENTS配置集成

---

## 📁 目录结构（完整功能已实现）

```
Universal-KB/
├── 01-raw/              # Layer 1: 原始资料（只读）
├── 02-processed/        # Layer 2: 处理后数据
├── 03-wiki/            # Layer 3: 知识图谱 ✅
│   ├── concepts/      # 概念定义 (3个页面)
│   ├── entities/      # 实体定义 (1个页面)
│   ├── sources/       # 源摘要
│   ├── comparisons/   # 对比分析
│   ├── index.md       # 知识图谱总索引 ✅
│   └── log.md        # 活动日志 ✅
├── 04-memory/          # Layer 4: 长期记忆 ✅
│   ├── memoryos.py    # MemoryOS引擎 ✅
│   ├── config.yaml   # 配置文件 ✅
│   ├── short_term/   # 短期记忆
│   ├── mid_term/    # 中期记忆
│   └── long_term/   # 长期记忆
├── 05-agents/          # Layer 5: AGENTS配置 ✅
│   └── AGENTS.md    # AI行为配置 ✅
├── 06-output/          # Layer 6: 输出成果
└── README.md           # 本文件 ✅
```

## ✅ 已实现功能

| 模块 | 状态 | 说明 |
|------|------|------|
| 目录结构 | ✅ | 6层完整架构 |
| MemoryOS | ✅ | 三层记忆引擎 |
| AGENTS配置 | ✅ | Ingest/Query/Lint流程 |
| 知识图谱 | ✅ | index + 4概念 + 1实体 |
| 链路串联 | ✅ | 完整内部链接 |

## 🔗 链路串联

```
AGENTS.md → 定义行为 →
  ├─ ingest → 01-raw → 03-wiki/sources → 03-wiki/concepts → index
  ├─ 查询 → 03-wiki/index → concepts/entities
  └─ lint → 03-wiki/log

memoryos.py →
  ├─ short_term (FIFO 7条)
  ├─ mid_term (热度1000条)
  └─ long_term (持久100条)
```

---

## 🚀 快速开始

### 1. 初始化

```bash
# 创建目录结构（自动生成）
mkdir -p Universal-KB/{01-raw,02-processed,03-wiki/{concepts,entities,sources,comparisons},04-memory/{short_term,mid_term,long_term},05-agents,06-output,docs}
```

### 2. 摄取知识

将原始文件放入 `01-raw/`，然后执行ingest流程。

### 3. 查询

查询 `03-wiki/` 下的知识图谱。

---

## 🔗 功能模块

| 模块 | 路径 | 功能 |
|------|------|------|
| Ingest | 01-raw → 03-wiki | 知识摄取 |
| Query | 03-wiki/ | 知识查询 |
| Lint | 03-wiki/ | 健康检查 |
| Memory | 04-memory/ | 长期记忆 |
| Agents | 05-agents/ | AI配置 |

---

## 📖 详细文档

- [架构设计](docs/architecture.md)
- [快速开始](docs/quickstart.md)

---

*本框架通用设计，无业务依赖，可直接交付使用*