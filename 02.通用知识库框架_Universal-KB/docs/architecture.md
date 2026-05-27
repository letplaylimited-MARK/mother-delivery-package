# Universal-KB 架构设计

> **版本**: V1.0  
> **日期**: 2026-04-21

---

## 一、核心理念

### 1.1 设计目标

- **通用**: 无业务依赖，可用于AI项目/数据库/知识管理
- **完整**: Ingest/Query/Lint 全套工作流
- **串联**: 所有模块无缝集成
- **交付**: 开箱即用

### 1.2 三层架构

```
          用户输入
              ↓
    ┌────────┴────────┐
    │   01-raw/       │  Layer 1: 原始资料
    │   (只读)        │
    └────────┬────────┘
              ↓
    ┌────────┴────────┐
    │   03-wiki/      │  Layer 2: 知识图谱
    │   (可编辑)      │  → concepts/entities/sources/
    └────────┬────────┘
              ↓
    ┌────────┴────────┐
    │   04-memory/   │  Layer 3: 长期记忆
    │   (持久化)      │  → MemoryOS引擎
    └────────────────┘
```

---

## 二、模块设计

### 2.1 知识图谱 (03-wiki/)

| 子目录 | 内容 | 格式 |
|--------|------|------|
| concepts/ | 概念定义 | MD + YAML Frontmatter |
| entities/ | 实体定义 | MD + YAML YAML |
| sources/ | 源摘要 | MD + YAML |
| comparisons/ | 对比分析 | MD表格 |

### 2.2 记忆系统 (04-memory/)

```
MemoryOS
├── ShortTermMemory (FIFO, 7条)
├── MidTermMemory (热度, 1000条)
└── LongTermMemory (持久化, 100条)
```

### 2.3 AGENTS配置 (05-agents/)

- Ingest流程：摄取知识
- Query流程：查询知识
- Lint流程：健康检查

---

## 三、数据流

### 3.1 Ingest流程

```
1. 放入文件 → 01-raw/
2. 读取分析 → 提取概念/实体
3. 创建 → 03-wiki/sources/源摘要
4. 更新 → 03-wiki/concepts/概念页
5. 更新 → 03-wiki/entities/实体页
6. 索引 → 03-wiki/index.md
7. 日志 → 03-wiki/log.md
```

### 3.2 Query流程

```
1. 接收查询 → 提取关键词
2. 搜索 → 03-wiki/concepts/
3. 搜索 → 03-wiki/entities/
4. 构建答案 → 引用相关页面
5. 返回结果
```

### 3.3 Memory流程

```
1. add_memory() → short_term (FIFO)
2. 淘汰 → mid_term (热度)
3. 晋升 → long_term (持久化)
```

---

## 四、状态

| 模块 | 状态 |
|------|------|
| 目录结构 | ✅ |
| 知识图谱 | ✅ |
| MemoryOS | ✅ |
| AGENTS | ✅ |
| 链路串联 | ✅ |

---

*本架构为通用框架，可直接交付使用*