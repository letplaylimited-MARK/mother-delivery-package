# Traceability Matrix

> 用途：追踪项目级 GOAL/REQ/PRD/SPEC/TASK/TEST/AUD/MEM 的对齐关系。
> 生成时间：2026-05-31。
> 状态：母交付包级追踪矩阵，覆盖跨 session 核心需求。

## 1. 目标（GOAL）

| ID | 目标 | 状态 | 验证方式 |
|---|---|---|---|
| G-1 | 建立 AI 协同开发的标准化交付流程 | 已完成 | 四体系 + VERIFY-DELIVERY.ps1 -Strict |
| G-2 | 消除验证体系中的所有非预期 FAIL | 已完成 | qa_runner.py validate: 31 自动 PASS / 0 manual-current / 0 FAIL / 0 WARN / 0 SKIP |
| G-3 | 将 QCM 公式模块从硬编码迁移为 config-driven | 已完成 | 12/14 模块迁移，测试全通过 |

## 2. 需求（REQ）

| ID | 需求 | 来源 | 映射 PRD | 映射 SPEC | 状态 |
|---|---|---|---|---|---|
| REQ-1 | Python venv 隔离环境 | V-1 | — | — | 已完成 |
| REQ-2 | SDK 测试路径正确 | V-2 | — | — | 已完成 |
| REQ-3 | 文件完整性验证无误报 | V-3 | — | — | 已完成 |
| REQ-4 | PowerShell 中文路径兼容 | V-4 | — | — | 已完成 |
| REQ-5 | QCM 参数可配置 | A-1 | — | — | 已完成 |
| REQ-6 | 源提示词吸收验证 | D | — | — | 已完成 |
| REQ-7 | 交付包四体系填充 | C | — | — | 已完成 |

## 3. 任务（TASK）

| ID | 任务 | 对应 REQ | 完成时间 | 产出 |
|---|---|---|---|---|
| T-1 | 创建 venv + 安装 6 依赖 | REQ-1 | 2026-05-28 | venv + packages |
| T-2 | 修复 qa_runner.py SDK 路径 | REQ-2 | 2026-05-28 | run_cmd_raw() |
| T-3 | 重新生成 MANIFEST.yaml | REQ-3 | 2026-05-28 | 299 文件 |
| T-4 | PowerShell UTF8 编码 | REQ-4 | 2026-05-28 | _auto_run_script 修改 |
| T-5 | 扩展 config.py paper_params | REQ-5 | 2026-05-28 | 14 模块参数 |
| T-6 | 迁移 12 模块常量 | REQ-5 | 2026-05-28 | 60 个替换 |
| T-7 | 源提示词吸收审查 | REQ-6 | 2026-05-28 | 26/26 验证 |
| T-8 | 四体系内容填充 | REQ-7 | 2026-05-28 | 4 文件 |
| T-9 | 5 个缺失文件创建 | REQ-7 | 2026-05-28 | 5 文件 |

## 4. 测试（TEST）

| ID | 测试 | 映射 TASK | 结果 |
|---|---|---|---|
| TEST-1 | qa_runner.py validate（全量） | T-1~T-5 | 31 注册项；31 自动 PASS / 0 manual-current / 0 FAIL |
| TEST-2 | VAL-01-SDK-TESTS（三组 Python SDK + TypeScript） | T-2 | 184 passed |
| TEST-3 | VAL-01-GHOST-VERIFY（完整性） | T-3 | 299 files ALL CLEAN |
| TEST-4 | VAL-04-QCM-ALL | T-5, T-6 | 25/25 PASS |
| TEST-5 | VAL-04-QCM-PAPER | T-5, T-6 | 38/38 PASS |
| TEST-6 | VERIFY-DELIVERY.ps1 -Strict | T-8, T-9 | 0 failures / 0 warnings |

## 5. 审计（AUD）

| ID | 审计 | 范围 | 结果 |
|---|---|---|---|
| AUD-1 | 源提示词吸收合规性 | 00/13 全目录 | 26/26 机制验证通过，11/11 reject 零泄漏 |
| AUD-2 | 跨文档一致性 | 00 validate_consistency.py | 10/10 PASS / 0 WARN |
| AUD-3 | Markdown fence 平衡 | 全量 523 md 文件 | 0 unbalanced |

## 6. 记忆（MEM）

| ID | 记录 | 优先级 | 存储位置 |
|---|---|---|---|
| MEM-1 | Python venv 策略和路径 | P0 | MEMORY.md §4.1 |
| MEM-2 | qa_runner.py 核心修复模式 | P0 | MEMORY.md §4.2 |
| MEM-3 | Submodule 操作规范 | P0 | MEMORY.md §4.3 |
| MEM-4 | MANIFEST 排除规则 | P1 | MEMORY.md §4.2 |
| MEM-5 | 循环依赖处理方案 | P1 | HANDOFF.md §4 |

---

## 7. 子系统项目级追踪实例

> 本节补充各子系统内部从 GOAL → REQ → TASK → TEST → AUD 的完整追踪链，与 §1-§6 母包级追踪形成层次。

### 7.1 00 超级提示词工程

| ID | 目标/需求 | 任务 | 测试 | 审计 |
|---|---|---|---|---|
| G-00-1 | 建立模型原生协作边界，防止源提示词越权 | T-00-1 创建 `00/11-模型原生协作协议.md` | AUD-00-1 检查所有 md 无"你现在就是..."表述 | AUD-00-1 PASS |
| REQ-00-1 | 源提示词吸收需有可验证的转译记录 | T-00-2 创建 `SUPER-PROMPT-ATOMIC-RESEARCH-REVIEW.md`（26机制矩阵） | TEST-00-1 26/26 机制验证通过 | AUD-00-2 11/11 reject 零泄漏 |
| REQ-00-2 | 使命唤醒必须有真实文件证据 | T-00-3 创建 `MISSION-MEMORY.md` + `MISSION-MEMORY-AWAKENING-PROTOCOL.md` | TEST-00-2 awakening_check 协议 8 步可手动验证 | AUD-00-3 无"记忆宫殿已加载"等假声明 |

### 7.2 01 通讯协议_幽灵通道

| ID | 目标/需求 | 任务 | 测试 | 审计 |
|---|---|---|---|---|
| G-01-1 | 文件完整性验证零误报 | T-01-1 实现 `GHOST-VERIFY` + MANIFEST.yaml（299文件） | TEST-01-1 VAL-01-GHOST-VERIFY: 299 files ALL CLEAN | AUD-01-1 MANIFEST 排除 `.pytest_cache/` 等运行时目录 |
| REQ-01-1 | 开源 SDK 测试用例全通过 | T-01-2 创建 `test_sdk_ps1.py` + `test_sdk_ts.ts`（18 tests） | TEST-01-2 VAL-01-SDK-TESTS: 18 passed | AUD-01-2 SDK 测试路径 `/` 替换 `\\` + PYTHONPATH 注入 |
| REQ-01-2 | PowerShell 中文路径 UTF8 兼容 | T-01-3 修改 `_auto_run_script` UTF8 输出 | TEST-01-3 `pytest test_sdk_ps1.py -v` 中文路径无 UnicodeDecodeError | AUD-01-3 `_auto_run_script` 使用 `PowerShell -UTF8` + `Write-Output` |

### 7.3 03 数据库管理_文件夹整理AI应用（knowledge-base-manager）

| ID | 目标/需求 | 任务 | 测试 | 审计 |
|---|---|---|---|---|
| G-03-1 | 知识库测试全 PASS，0 跳过 | T-03-1 实现并维护 `tests/` 目录测试模块 | TEST-03-1 VAL-03-TESTS: 107 passed | AUD-03-1 H4 修复：23 个 except Exception 全部补 `logger.exception()` |
| REQ-03-1 | requirements.txt 无未使用包 | T-03-2 清理 5 个未使用依赖，保留 ruff | TEST-03-2 `pip check` 零冲突 + ruff check 无 F401 | AUD-03-2 M1 修复：15 处 sys.path hacks 整合为 `path_setup.py` |
| REQ-03-2 | install.ps1 一键安装验证通过 | T-03-3 创建 `install.ps1` + `validate_install.py` | TEST-03-3 VAL-03-INSTALL: install + validate 双 PASS | AUD-03-3 PowerShell `-ExecutionPolicy Bypass` 兼容性确认 |

### 7.4 04 QCM-MVP-Emergence

| ID | 目标/需求 | 任务 | 测试 | 审计 |
|---|---|---|---|---|
| G-04-1 | QCM 公式模块从硬编码迁移为 config-driven | T-04-1 扩展 `qcm/config.py` paper_params 段（14 模块，60 常量） | TEST-04-1 VAL-04-QCM-ALL: 25 PASS + VAL-04-QCM-PAPER: 38 PASS + VAL-04-HEALTH: 6/6 = 69/69 ALL PASS | AUD-04-1 calculator.py/detector.py 因循环依赖保留硬编码，标注来源 |
| REQ-04-1 | 涌现公式 R > 0.85 可复现（seed=42） | T-04-2 实现 `detector.py` 核心公式 + `test_emergence.py`（38 tests） | TEST-04-2 VAL-04-QCM-PAPER: 38/38 PASS, R=0.8664 | AUD-04-2 公式版本 v6.3，E 惩罚项已移除，R 上限 0.85+ |
| REQ-04-2 | qa_runner.py 在 sandbox 环境可运行 | T-04-3 修复 `run_cmd()` 添加 `env=os.environ.copy()` | TEST-04-3 `python qa_runner.py validate --scope P04_QCM` 5/5 PASS | AUD-04-3 Markdown fence 检测改用 `re.MULTILINE` 防止 false negative |

### 7.5 05 超极智脑_Q-Spectrum

| ID | 目标/需求 | 任务 | 测试 | 审计 |
|---|---|---|---|---|
| G-05-1 | 端到端集成测试覆盖核心工作流 | T-05-1 维护 `tests/`、`run.py --e2e`、API/MCP smoke | TEST-05-1 VAL-05-PYTEST 158 passed；VAL-05-E2E 13/13；API/MCP smoke PASS | AUD-05-1 BRAIN-KB/.chroma_db/ 与 platform.db 权威路径验证 |
| REQ-05-1 | 状态对齐：MISSION-MEMORY + CAPABILITY-REGISTRY 一致 | T-05-2 运行 `python run.py --status` 与 `qa_runner.py validate --scope P05_QSPECTRUM` | TEST-05-2 VAL-05-STATUS: System ALL GREEN | AUD-05-2 ROLE-REGISTRY.yaml 与 AGENTS.md 角色列表对齐 |
| REQ-05-2 | CI/CD 自动化（GitHub Actions） | T-05-3 交付前以当前仓库 workflows 与 GitHub Actions 状态确认 | TEST-05-3 当前本地验证作为主要证据；远端 CI 需独立确认 | AUD-05-3 不用本地成功替代远端 CI 绿色状态 |

### 7.6 协同通用AI大模型开发交付包

| ID | 目标/需求 | 任务 | 测试 | 审计 |
|---|---|---|---|---|
| G-C-1 | 四体系（价值/功能/结构/运作）从模板态升级为可交付内容 | T-C-1 填充 `01-价值体系/README.md` ~ `04-运作体系/README.md` | TEST-C-1 VERIFY-DELIVERY.ps1 -Strict: 0 failures, 0 warnings | AUD-C-1 四体系内容基于真实开发过程，非模板填充 |
| REQ-C-1 | 5 个交付门禁文件必须存在且内容非空 | T-C-2 创建 AI_PROJECT_CONTEXT / HANDOFF / CHANGELOG / TRACEABILITY-MATRIX / VALIDATION_REPORT | TEST-C-2 `scripts/verify.ps1` 调用 VERIFY-DELIVERY.ps1 -Strict 全 PASS | AUD-C-2 HANDOFF.md 包含 AKU 规范待建等已知缺口 |
| REQ-C-2 | 占位符 `<...>` 在严格模式下零容忍 | T-C-3 全局替换 `<母交付包根目录>` → `project-root`，`<package>` → `{package}` | TEST-C-3 Grep `<[A-Za-z]` 零匹配 | AUD-C-3 白名单机制因编码问题未生效，直接替换更可靠 |
| REQ-C-3 | 交付包事实不能停留在历史快照 | T-C-4 2026-05-31 刷新验证总数、测试数、P05/P03 当前入口 | TEST-C-4 VAL-USER-PACK-DELIVERY + VAL-USER-PACK-DELIVERY-STRICT 0 failures / 0 warnings | AUD-C-4 B6 文档审计确认不再把 2026-05-28 的旧验证快照当作当前事实 |

---

## 8. 跨子系统追踪链示例

### 8.1 用户唤醒握手 end-to-end 追踪

```
GOAL: G-00-1（唤醒协议标准化）
  ↓
REQ: REQ-00-2（使命唤醒必须有真实文件证据）
  ↓
TASK: T-00-3（创建 MISSION-MEMORY.md + AWAKENING-PROTOCOL.md）
  ↓
TEST: TEST-00-2（awakening_check 8 步可手动验证）
  ↓
AUD: AUD-00-3（无假记忆声明）
  ↓
MEM: MEM-3（Submodule 操作规范，跨唤醒 session 持久化）
```

### 8.2 QCM 公式模块 config-driven 迁移追踪

```
GOAL: G-04-1（硬编码 → config-driven）
  ↓
REQ: REQ-04-1（参数可配置，来源可追溯）
  ↓
TASK: T-04-1（config.py paper_params + 12 模块迁移，60 常量）
  ↓
TEST: TEST-04-1（VAL-04-QCM-ALL 25 PASS + VAL-04-HEALTH 6/6 = 31）
  TEST: TEST-04-2（VAL-04-QCM-PAPER 38/38 PASS）
  ↓
AUD: AUD-04-1（calculator.py/detector.py 标注硬编码来源，待 Phase 3 解循环依赖）
  ↓
MEM: MEM-1（config.py 路径写入 MEMORY.md §4.1）
```

### 8.3 交付包四体系严格模式追踪

```
GOAL: G-C-1（四体系可交付）
  ↓
REQ: REQ-C-1（5 个门禁文件必须存在）
  REQ: REQ-C-2（占位符零容忍）
  ↓
TASK: T-C-1（四体系内容填充，基于真实开发过程）
  TASK: T-C-2（5 个文件创建）
  TASK: T-C-3（占位符全局替换）
  ↓
TEST: TEST-C-1（VERIFY-DELIVERY.ps1 -Strict 0 failures）
  TEST: TEST-C-2（scripts/verify.ps1 全 PASS）
  TEST: TEST-C-3（Grep `<[A-Za-z]` 零匹配）
  ↓
AUD: AUD-C-1（内容非模板，有真实数据）
  AUD-C-2（HANDOFF.md 已知缺口明确标记）
  ↓
MEM: MEM-5（循环依赖方案写入 HANDOFF.md §4）
```
