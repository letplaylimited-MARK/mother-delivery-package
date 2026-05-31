# 02.通用知识库框架 Universal-KB -- INDEX

> 定位: 通用知识库**模板规范** | 版本: V2.1 | 2026-05-29
> 关系: 本目录 = 模板 / 03 目录 = 可运行实现 (Flask + FAISS + MCP)
> 说明: 本目录内不包含单独的 `V1_TO_V2_MIGRATION.md`；迁移路径见 README 的方案 A/B 与母包根目录同名迁移文档。

## 文件结构
```
02.通用知识库框架_Universal-KB/
├── README.md
├── 01-raw/                            原始资料 (只读, ingest 入口)
├── 02-processed/                      处理后数据
├── 03-wiki/                           知识图谱
│   ├── concepts/        概念定义 (AKU 规范兼容)
│   ├── entities/        实体定义
│   ├── sources/         源摘要
│   ├── comparisons/     对比分析
│   ├── index.md         知识图谱总索引
│   └── log.md           活动日志
├── 04-memory/                         长期记忆 (MemoryOS 引擎)
│   ├── memoryos.py      概念引擎 (三层: short/mid/long)
│   ├── config.yaml      记忆配置
│   ├── short_term/      短期记忆
│   ├── mid_term/        中期记忆
│   └── long_term/       长期记忆
├── 05-agents/                         AGENTS 配置
│   └── AGENTS.md         Ingest / Query / Lint 三流程
├── 06-output/                         输出成果
└── docs/                              补充文档
```

## 关键入口
| 文件 | 用途 | 优先级 |
|------|------|--------|
| README.md | 模板定位、与 03 实现版的关系、快速开始 A/B | 高 |
| 03-wiki/index.md | 知识图谱总索引 | 高 |
| 04-memory/memoryos.py | MemoryOS 概念引擎 (编译运行验证) | 中 |
| 04-memory/config.yaml | 记忆配置 (FIFO 7 / 热度 1000 / 持久 100) | 中 |
| 05-agents/AGENTS.md | Ingest / Query / Lint 工作流定义 | 中 |
| 母包根目录 `V1_TO_V2_MIGRATION.md` | 本模板到 03 实现版的迁移指引 | 低 |

## 快速开始

方案 A: 直接使用 03 实现版 (推荐)
```
cd "03.数据库管理_文件夹整理AI应用"
pip install -r requirements.txt
pytest tests/ -q        # 当前审计 107 passed
python app.py           # 启动 Flask 知识库服务
```

方案 B: 基于本模板自建
```
cp -r "02.通用知识库框架_Universal-KB" your-project-kb/
mkdir -p 01-raw 02-processed 03-wiki/{concepts,entities,sources,comparisons} \
         04-memory/{short_term,mid_term,long_term} 05-agents 06-output docs
```

Windows PowerShell:
```powershell
Copy-Item -Recurse -Force "02.通用知识库框架_Universal-KB" "your-project-kb"
cd your-project-kb
New-Item -ItemType Directory -Force -Path `
  01-raw,02-processed,03-wiki\concepts,03-wiki\entities,03-wiki\sources,03-wiki\comparisons,`
  04-memory\short_term,04-memory\mid_term,04-memory\long_term,05-agents,06-output,docs
```

验证: `python -m py_compile 04-memory/memoryos.py` -- 无语法错误即通过

## 核心流程
```
Ingest:  原始文件 -> 01-raw/ -> 03-wiki/sources/ -> concepts/ -> index.md
Query:   用户查询 -> 03-wiki/index.md -> concepts/ + entities/ -> 返回结果
Lint:    触发 -> 03-wiki/log.md -> 断链检测 + 30天过期检测
Memory:  short_term (FIFO 7) -> mid_term (热度 1000) -> long_term (持久 100)
```
