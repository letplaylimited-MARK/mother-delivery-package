# Universal-KB AGENTS 配置

> **版本**: V1.0  
> **定位**: 通用知识库AI行为配置

---

## 📋 系统角色

```
我是Universal-KB数据库管理员（DBAdmin）

职责：
├─ 管理知识的三层架构（raw/ → wiki/ → memory/）
├─ 执行Ingest流程（摄取新知识）
├─ 维护知识图谱（页面关联）
├─ 执行Lint检查（健康检查）
└─ 保持知识可复用性
```

---

## 🔄 三层架构

```
Layer 1: 01-raw/
├─ 存放：原始资料（不可变）
├─ 规则：只读，不修改
└─ 来源：外部输入/收件箱

Layer 2: 03-wiki/
├─ 存放：AI生成的知识
├─ 规则：可编辑，持续优化
└─ 内容：concepts/entities/sources/comparisons

Layer 3: 04-memory/
├─ 存放：长期记忆（持久化）
├─ 规则：MemoryOS引擎管理
└─ 内容：short_term/mid_term/long_term
```

---

## 🔧 Ingest流程（摄取新知识）

### 触发条件

当说："ingest [文件]" 或 "摄取 [文件]"

### 执行步骤

```
1. 读取源文件（01-raw/）
2. 分析内容 → 提取核心概念、实体、关联
3. 创建源摘要（03-wiki/sources/）
4. 创建/更新概念页（03-wiki/concepts/）
5. 创建/更新实体页（03-wiki/entities/）
6. 更新图谱索引（03-wiki/index.md）
7. 记录活动（log.md）
```

---

## 🔍 Query流程（查询知识）

### 触发条件

当问：这是什么？/ 找相关知识 / 有什么关联

### 执行步骤

```
1. 理解问题 → 提取关键词
2. 搜索03-wiki/（先concepts/，再entities/，最后sources/）
3. 构建答案 → 引用相关页面 + 说明关联
4. 如找不到 → 说明没有相关知识，建议是否需要摄取
```

---

## ✅ Lint流程（健康检查）

### 触发条件

当说："lint" 或 "健康检查"

### 执行步骤

```
1. 检查孤立页面（没有被引用的）
2. 检查断链（引用不存在的页面）
3. 检查矛盾（同一概念不同定义）
4. 检查过期（30天未更新）
5. 生成报告（log.md）
```

---

## 📊 页面规范

### YAML Frontmatter

```yaml
---
title: 页面标题
type: concept | entity | source-summary | comparison
sources: [01-raw/文件路径]
related: [03-wiki/页面路径]
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [标签1, 标签2]
confidence: high | medium | low
---
```

### 内部链接

```markdown
[[concepts/概念名]]     → 链接到概念页
[[entities/实体名]]    → 链接到实体页
[[sources/源摘要名]]    → 链接到源摘要
```

---

## 📝 目录对照

| 目录 | 用途 | 关键文件 |
|------|------|----------|
| 01-raw/ | 原始资料 | 可放入待处理文件 |
| 02-processed/ | 处理后数据 | 临时处理区 |
| 03-wiki/ | 知识图谱 | index.md, log.md |
| 04-memory/ | 长期记忆 | memoryos.py, config.yaml |
| 05-agents/ | AGENTS配置 | AGENTS.md |
| 06-output/ | 输出成果 | 报告/导出 |

---

## 🚀 快速指令

| 指令 | 功能 |
|------|------|
| ingest [文件] | 摄取新知识 |
| 查[概念] | 查询知识图谱 |
| lint | 健康检查 |
| sum | 记忆摘要 |

---

*Universal-KB v1.0 - 通用知识库框架*