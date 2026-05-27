# Ingest流程

> **类型**: concept  
> **置信度**: high

---

## 定义

知识摄取SOP，将01-raw/中的原始资料转化为03-wiki/中的结构化知识。

---

## 流程步骤

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

## 触发条件

当说："ingest [文件]" 或 "摄取 [文件]"

---

## 关联

- 三层架构: [三层架构](./三层架构.md)
- Lint检查: [Lint检查](./Lint检查.md)

---

## 示例

```
ingest 01-raw/新文档.md
→ 分析文件内容
→ 创建 03-wiki/sources/新文档.md
→ 更新 03-wiki/concepts/相关概念.md
→ 记录到 log.md
```