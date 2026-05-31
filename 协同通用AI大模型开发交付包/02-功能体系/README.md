# 功能体系

> 用途：说明项目具体能做什么、用户如何使用、AI 能力边界在哪里。
> 生成时间：2026-05-31，基于母交付包七子系统与 QCM Skill 能力包的当前验证结果。

## 1. 功能总览

| 功能 | 用户价值 | 输入 | 输出 | 状态 |
|---|---|---|---|---|
| AI 标准唤醒握手 | 新模型/新会话零成本理解项目 | MISSION-MEMORY.md + 唤醒协议 | awakening_check YAML + 路由决策 | 已完成 |
| 意图识别与路由 | 自然语言输入自动进入正确子系统 | 用户自然语言请求 | 路由目标 + 置信度 + 最小文件清单 | 已完成 |
| SpecForge PRD/SPEC 锻造 | 模糊需求转化为可开发、可测试的规格 | 自然语言需求描述 | PRD + SPEC + TEST + ADR 文档 | 已完成 |
| QCM 共鸣/涌现分析 | 多角色协同质量评估，检测涌现行为 | 角色对话数据 | R 值 + 涌现等级 + 22 公式分析 | 已完成 |
| Ghost Channel 通信协议 | 多智能体记忆同步、因果一致性、增量同步 | 多 Agent 消息流 | Delta 同步 + Vector Clock + 完整性校验 | 已完成 |
| 知识库管理（MCP） | 文件整理、向量检索、知识沉淀 | 文件/文本/查询 | 搜索结果 + 知识条目 + 向量索引 | 已完成 |
| Q-SpecTrum 平台 | 15 角色统一调度、Web UI、API、知识库闭环 | 自然语言对话 | Web 聊天 + REST API + 任务追踪 | 已完成 |
| Skill/MCP 能力配置 | 新能力选型、评估、安装、集成验证 | 能力需求描述 | 技能需求清单 + 能力卡 + 配置方案 | 已完成 |
| 全链路审计 | 跨子系统数据流/业务流/运行流对齐检查 | 项目目录 | 审计报告 + 断裂点矩阵 + 修复建议 | 已完成 |
| 验证证据链 | 自动化验证 30 个注册项（测试/安装/集成/一致性/运行烟测） | 项目目录 | qa_runner.py validate 报告 | 已完成 |
| 反漂移控制 | 防止需求/规格/语义漂移和反复重构 | PRD/SPEC 变更请求 | 漂移评估 + 阶段门守门决策 | 已完成 |
| 用户交付包组装 | 从母包抽取项目成果，生成可交付的四体系文档 | 母包 + 项目事实 | 价值/功能/结构/运作四体系文档 | 模板已建 |

## 2. 用户流程

### 2.1 首次进入项目

```text
开发者打开母交付包根目录
  -> 任何 AI 模型读取 MISSION-MEMORY.md
  -> 完成 8 步标准唤醒握手（输出 awakening_check）
  -> 引导秘书识别意图、推荐路由
  -> 进入目标子系统开始工作
```

### 2.2 项目开发流程

```text
自然语言描述需求
  -> 引导秘书意图识别（5D 雷达 + 13 种意图分类）
  -> 置信度评估（DIRECT/CONFIRM/CLARIFY）
  -> SpecForge Gate 1: 蓝图锚定（问题/用户/指标/边界）
  -> SpecForge Gate 2: 功能锻造（用户故事/流程/异常/验收）
  -> SpecForge Gate 3: 质量熔炼（性能/安全/兼容/UX 7 维度）
  -> SpecForge Gate 4: 淬火交付（完整性/一致性/风险审查）
  -> 原子治理：PRD->SPEC->TASK->TEST->AUD->MEM 追踪
  -> 子系统执行（代码/测试/知识库/协议）
  -> 验证证据链（qa_runner.py validate）
  -> 用户交付包四体系填充 + VERIFY-DELIVERY.ps1 -Strict
```

### 2.3 AI 协同开发流程

```text
主 AI 通过引导秘书分配任务
  -> 角色沙盘选择角色子集（3 种强度）
  -> 多角色并行推演/开发
  -> 产出 Context Pack 或 Handoff
  -> 下一个 AI（或同一 AI 新会话）通过 Handoff 继续工作
  -> 结果写入真实文件、验证记录或交接文档
  -> 任务态角色回收（不是永久人格）
```

## 3. AI 能力

| AI 能力 | 触发方式 | 使用数据 | 输出 | 人工确认点 |
|---|---|---|---|---|
| 意图路由 | 自动（自然语言输入时） | 用户请求文本 | 路由目标 + 置信度评分 | CONFIRM 级别需人工确认 |
| PRD/SPEC 锻造 | 进入 SpecForge Gate 后自动 | 自然语言需求 + 项目上下文 | PRD/SPEC/TEST 文档 | Gate 1-4 各阶段需人工审批 |
| QCM 分析 | 调用 04 子系统 | 角色对话数据 | R 值 + 涌现检测报告 | 涌现等级判定需人工确认 |
| 知识库检索 | MCP 工具调用 | 向量索引 + 关键词 | 搜索结果 + 相关度排序 | 高风险操作需确认 |
| 代码生成 | 子系统执行阶段 | PRD/SPEC + 项目代码 | 源码 + 测试 | 测试通过后确认 |
| 审计分析 | 手动触发或定期 | 项目全目录 | 审计报告 + 断裂点列表 | 修复方案需人工审批 |
| 交付验证 | 手动触发 | 交付包目录 | PASS/FAIL + 失败详情 | FAIL 需人工修复后重跑 |

## 4. 配置与权限

| 项 | 说明 |
|---|---|
| 账号/权限 | 本地项目无账号系统；Git 使用 SSH/HTTPS 认证；AI 模型服务由用户自行管理 API Key |
| 配置项 | `qcm/config.py`（QCM 参数）、`05/brain_core/config.py`（平台参数）、各子系统 `requirements.txt` 或 `pyproject.toml` |
| 外部依赖 | Python 3.10+、Git、ChromaDB（向量检索）、Flask（Web 服务）、通用 AI 大模型 API（用户自备） |

## 5. 异常与失败处理

| 异常 | 用户可见表现 | 处理方式 |
|---|---|---|
| 循环导入 | `ImportError: cannot import name` | 04 子系统 calculator/detector 已使用模块级默认值 + config 注释标注，避免循环 |
| 中文路径乱码 | PowerShell 输出显示乱码 | `_auto_run_script` 中添加 UTF-8 编码设置 |
| MANIFEST hash 不匹配 | VERIFY.ps1 报告 failed files | 重新生成 MANIFEST.yaml（排除 `.pytest_cache`/`__pycache__`） |
| venv 依赖缺失 | `ModuleNotFoundError` | 进入对应子系统后创建 Python venv，并优先执行 `pip install -r requirements.txt` |
| Submodule 指针偏移 | `git diff` 显示 submodule 脏 | 在子模块内 commit+push，再在根目录更新指针 commit |
| 幻觉完成 | AI 声称已完成但无证据 | E0-E4 证据等级体系，E0 必须标注"推测/待验证"；沙盘结论必须进入 TEST/AUD |
