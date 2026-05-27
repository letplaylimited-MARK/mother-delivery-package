# Universal-KB 知识图谱总索引

> **版本**: V1.0  
> **更新时间**: 2026-05-12

---

## 图谱结构

```
03-wiki/
├── concepts/       # 概念定义
├── entities/      # 实体定义
├── sources/       # 源摘要
├── comparisons/   # 对比分析
├── index.md       # 本索引
└── log.md        # 活动日志
```

---

## 概念页 (concepts/)

| 概念 | 定义 | 关联 |
|------|------|------|
| [[concepts/三层架构]] | raw→wiki→memory | [[entities/系统]] |
| [[concepts/Ingest流程]] | 知识摄取SOP | [[concepts/三层架构]] |
| [[concepts/Lint检查]] | 健康检查SOP | [[concepts/Ingest流程]] |

---

## 实体页 (entities/)

| 实体 | 属性 | 关联 |
|------|------|------|
| [[entities/系统]] | name, version, layers | [[concepts/三层架构]] |

---

## 源摘要 (sources/)

| 源文件 | 要点 | 关联 |
|--------|------|------|
| [[sources/框架说明]] | Universal-KB设计要点 | [[concepts/三层架构]] |

---

## 对比分析 (comparisons/)

| 比较项 | 结论 |
|--------|------|
| [[comparisons/传统-vs-Universal-KB]] | 传统文件夹 vs 本系统 — 显著优势 |

---

## 操作命令

```
# 摄取新知识
ingest 01-raw/文件名

# 查询概念
查 [概念名]

# 健康检查
lint
```

---

## 最近活动

| 日期 | 操作 | 内容 |
|------|------|------|
| 2026-04-21 | 创建 | 初始化知识图谱 |

---

*本索引由系统自动维护*
