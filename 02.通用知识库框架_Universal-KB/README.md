# Universal-KB 通用知识库框架

> **版本**: V2.1 | **更新**: 2026-05-29
> **定位**: 通用知识库**模板规范**。`03.数据库管理_文件夹整理AI应用/` 是本模板的完整可运行实现（Flask + FAISS + MCP）。
> **关系**: 本目录 = 模板 / `03` = 实现。迁移路径由本 README 的方案 A/B 和根目录 `V1_TO_V2_MIGRATION.md` 共同说明；本模板目录内不另带迁移文件。

---

## 核心定位

| 项目 | 类型 | 技术栈 | 状态 |
|------|------|----------|------|
| **02 Universal-KB**（本目录） | 模板规范 | Markdown + Python 脚本 | 模板态 |
| **03 knowledge-base-manager** | 可运行实现 | Flask + FAISS + MCP + ChromaDB | ✅ 生产级（当前审计 107/107 tests） |

**使用选择**：
- 需要**快速开始 / 轻量部署** → 直接使用 `03/` 的 V2.0 实现
- 需要**自定义模板 / 学习架构** → 参考本目录结构

---

## 目录结构（6 层完整架构）

```
Universal-KB/
├── 01-raw/              # Layer 1: 原始资料（只读， ingest 入口）
├── 02-processed/        # Layer 2: 处理后数据（可选）
├── 03-wiki/            # Layer 3: 知识图谱
│   ├── concepts/      # 概念定义（AKU 规范兼容）
│   ├── entities/      # 实体定义
│   ├── sources/       # 源摘要（映射 AKU source 字段）
│   ├── comparisons/   # 对比分析
│   ├── index.md       # 知识图谱总索引
│   └── log.md        # 活动日志
├── 04-memory/          # Layer 4: 长期记忆（MemoryOS 引擎）
│   ├── memoryos.py    # MemoryOS 概念引擎（三层设计：short/mid/long）— 可编译运行，完整实现见 03/
│   ├── config.yaml   # 记忆配置（FIFO 7 / 热度 1000 / 持久 100）— 概念规格
│   ├── short_term/   # 短期记忆目录（当前 session）
│   ├── mid_term/     # 中期记忆目录（热度排序）
│   └── long_term/   # 长期记忆目录（持久化）
├── 05-agents/          # Layer 5: AGENTS 配置（AI 行为定义）
│   └── AGENTS.md    # Ingest / Query / Lint 三流程
├── 06-output/          # Layer 6: 输出成果（交付物）
├── docs/               # 补充文档
├── README.md           # 本文件
└── docs/               # 模板文档；迁移说明见本 README 方案 A/B 与根目录 V1_TO_V2_MIGRATION.md
```

---

## 核心功能

### 1. 知识摄取（Ingest）

```
原始文件 → 01-raw/
  → 03-wiki/sources/（源摘要）
  → 03-wiki/concepts/（概念提取，符合 AKU 规范）
  → 03-wiki/index.md（知识图谱索引更新）
```

**AKU 规范对接**：摄取的每条概念自动生成 `aku_id:` frontmatter（参见 `00/13-源提示词吸收与演化/AKU-KNOWLEDGE-ATOM-SPEC.md`）

### 2. 知识查询（Query）

```
用户查询 → 03-wiki/index.md → concepts/ + entities/
  → 如启用 05 Q-Spectrum BRAIN-KB：向量检索 .chroma_db/
```

### 3. 知识健康检查（Lint）

```
Lint 触发 → 03-wiki/log.md（检查知识图谱完整性）
  → 断链检测（AKU links: [] 中的无效引用）
  → 过期检测（超过 30 天未 re-verified 的 AKU）
```

### 4. 长期记忆（MemoryOS）

```
memoryos.py 三层引擎：
  - short_term: FIFO 7 条（当前 session）
  - mid_term:   热度排序 1000 条（跨 session）
  - long_term:  持久化 100 条（核心知识锚点）
```

**与 MISSION-MEMORY 对接**：每次唤醒时读取 `04-memory/long_term/` 中的 High 置信度 AKU，作为唤醒上下文。

---

## 快速开始

### 方案 A：直接使用 03/ 可运行版（推荐）

```bash
# 克隆母交付包
git clone https://github.com/letplaylimited-MARK/mother-delivery-package.git
cd mother-delivery-package

# 进入 03 实现版
cd "03.数据库管理_文件夹整理AI应用"

# 创建 Python venv（使用系统 Python 3.10+）
python -m venv .venv
.venv/Scripts/activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# 安装依赖
pip install -r requirements.txt

# 运行测试（当前审计：107 passed）
pytest tests/ -q

# 启动 Flask 知识库服务
python app.py
```

### 方案 B：基于本模板自建

```bash
# Linux/macOS/Git Bash：复制本目录为项目起点
cp -r "02.通用知识库框架_Universal-KB" your-project-kb/

# 初始化目录结构（Linux/macOS/Git Bash）
cd your-project-kb/
mkdir -p 01-raw 02-processed 03-wiki/{concepts,entities,sources,comparisons} \
         04-memory/{short_term,mid_term,long_term} 05-agents 06-output docs

# 将 MemoryOS 引擎放入 04-memory/
# （从 03/ 实现版复制 memoryos.py 和 config.yaml）
```

```powershell
# Windows PowerShell：复制本目录为项目起点
Copy-Item -Recurse -Force "02.通用知识库框架_Universal-KB" "your-project-kb"

# Windows PowerShell 初始化目录结构
cd your-project-kb
New-Item -ItemType Directory -Force -Path `
  01-raw,02-processed,03-wiki\concepts,03-wiki\entities,03-wiki\sources,03-wiki\comparisons,`
  04-memory\short_term,04-memory\mid_term,04-memory\long_term,05-agents,06-output,docs
```

---

## 与母包其他子系统的接口

| 对接目标 | 接口方式 | 说明 |
|-----------|----------|------|
| **00 超级提示词工程** | `AKU-KNOWLEDGE-ATOM-SPEC.md` | 知识原子格式规范，ingest 时自动生成 AKU frontmatter |
| **03 knowledge-base-manager** | 直接调用 Flask API | 本模板的 ingest/query/lint 流程即 03 的核心工作流 |
| **05 Q-Spectrum BRAIN-KB** | `.chroma_db/` 向量库 | 03-wiki/ 的概念可同步写入 BRAIN-KB 向量检索 |
| **协同交付包** | `03-wiki/index.md` | 项目知识图谱作为交付包的一部分 |

---

## 验证方式

| 验证项 | 工具 | 通过条件 |
|--------|------|----------|
| 目录结构完整性 | 手动检查 | 6 层目录全部存在 |
| MemoryOS 编译 | `python -m py_compile memoryos.py` | 无语法错误 |
| MemoryOS smoke | `python memoryos.py` | 概念脚本可运行 |
| AKU frontmatter 格式 | 手动检查 | 所有 `aku_id:` 字段符合 `00/13/AKU-KNOWLEDGE-ATOM-SPEC.md` 规范 |

---

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| V2.1 | 2026-05-29 | 升级 README：明确与 03 实现版的关系，补充 AKU 对接规范，移除占位符 |
| V1.0 | 2026-04-21 | 初始模板版本（6 层架构定义） |
| V2.0 | 2026-05-23 | 03/ 实现版完成（Flask + FAISS + MCP；当前审计已扩展到 107 tests） |

---

## 模板范围说明

本目录为**设计模板**，以下功能在 `03.数据库管理_文件夹整理AI应用/` 中有完整实现：

- ✅ AKU 批量验证 — 03/ 的 `verify_install.py` 包含知识库完整性检查
- ✅ MemoryOS 完整实现 — 03/ 的 `.workbuddy/记忆层/` 含持久化记忆引擎
- ✅ BRAIN-KB 双向同步 — 03/ 的 `mcp_server.py` 提供向量检索接口，可与 05/ 对接

---

*本框架通用设计，无业务依赖。可运行实现见 `03.数据库管理_文件夹整理AI应用/`*
