# 运作体系

> 用途：说明项目如何安装、启动、验证、维护、升级、排错和交接。
> 生成时间：2026-05-28，基于实际验证和操作记录。

## 1. 环境要求

| 项 | 要求 |
|---|---|
| 操作系统 | Windows 10/11（已验证）；macOS/Linux 原理兼容但未测试 |
| 运行时 | Python 3.13+（推荐 3.13.12） |
| 网络 | pip install 需联网下载依赖；AI 模型 API 需联网（用户自备） |
| 模型/API | 任意通用 AI 大模型（DeepSeek/元宝/Claude/GPT/Gemini 等），API Key 由用户自行管理 |
| Git | 支持 submodule（03→main, 05→master） |
| 磁盘 | 约 50MB（代码+文档），不含 venv 和数据库 |

## 2. 安装步骤

```powershell
# 1. 克隆仓库（GitHub 仓库：letplaylimited-MARK/mother-delivery-package）
git clone https://github.com/letplaylimited-MARK/mother-delivery-package.git
cd mother-delivery-package

# 2. 初始化 submodule
git submodule update --init --recursive

# 3. 创建 Python 虚拟环境
python -m venv .venv

# 4. 安装核心依赖
.venv\Scripts\pip install cryptography flask numpy chromadb pytest pytest-asyncio
```

需要配置的环境变量或配置项：

| 配置项 | 用途 | 示例写法 |
|---|---|---|
| PYTHONUTF8 | 避免中文路径编码问题（Windows PowerShell） | `$env:PYTHONUTF8='1'` |
| AI API Key | 调用通用 AI 大模型（如需 AI 功能） | 按模型服务商文档配置，不写真实密钥 |

## 3. 启动方式

### 3.1 Q-SpecTrum 主平台

```powershell
cd "project-root\05.超极智脑_Q-SpecTrum"
$env:PYTHONUTF8='1'
python run.py --web          # 启动 Web UI（端口 8765）
python run.py --status       # 健康检查（31/31 OK）
python run.py --query "你的问题"  # 单次查询
```

启动成功的标志：
- Web UI 在 `http://localhost:8765` 可访问
- `--status` 显示 `System: ALL GREEN`

### 3.2 知识库应用

```powershell
cd "project-root\03.数据库管理_文件夹整理AI应用"
python verify_install.py     # 安装验证（22 通过）
python app.py --port 5000    # 启动 Web 服务
```

### 3.3 MCP Server

```powershell
cd "project-root\03.数据库管理_文件夹整理AI应用"
python mcp_server.py         # 启动 MCP Server（stdio 模式）
```

## 4. 验证方式

### 4.1 全量验证（18 条检查）

```powershell
cd "project-root"
python qa_runner.py validate
```

验收标准：

| 项 | 通过标准 |
|---|---|
| 安装 | VAL-03-INSTALL PASS（verify_install 22 通过） |
| QCM 测试 | VAL-04-QCM-ALL PASS（25 tests） |
| QCM 论文 | VAL-04-QCM-PAPER PASS（38 tests） |
| SDK 测试 | VAL-01-SDK-TESTS PASS（18 tests 开源 SDK） |
| Ghost Channel | VAL-01-GHOST-VERIFY PASS（299 文件 ALL CLEAN） |
| 集成验证 | VAL-05-INTEGRATION PASS（verify-integration 31 OK） |
| 总体 | FAIL 数 ≤ 1（仅 VAL-USER-PACK-DELIVERY-STRICT 模板项） |

### 4.2 交付验证（严格模式）

```powershell
cd "project-root\协同通用AI大模型开发交付包"
powershell -ExecutionPolicy Bypass -File .\VERIFY-DELIVERY.ps1 -Strict
```

验收标准：`PASS: delivery package base verification completed.`，零 FAIL。

### 4.3 子系统独立验证

```powershell
# 01 Ghost Channel
cd "project-root\01.通讯协议_幽灵通道"
powershell -ExecutionPolicy Bypass -File .\VERIFY.ps1

# 04 QCM
cd "project-root\04.QCM-MVP-Emergence"
python "02-代码编写\test_qcm_all.py"
pytest "02-代码编写\test_roles.py" "02-代码编写\test_collaboration.py" -q

# 05 Q-SpecTrum
cd "project-root\05.超极智脑_Q-SpecTrum"
python verify-integration.py
```

## 5. 日常维护

| 事项 | 频率 | 操作 |
|---|---|---|
| Git 同步 | 每次修改后 | 子模块内 commit+push，根目录更新指针后 commit+push |
| 验证运行 | 每次提交前 | `python qa_runner.py validate` |
| MANIFEST 更新 | 文件变更后 | 重新生成 `01/MANIFEST.yaml`（排除 cache 目录） |
| 知识库索引 | 新文件入库后 | `python app.py --ingest` 或 MCP `process_file` |
| 数据库备份 | 按需 | 复制 `platform.db` 和 `search_index.db` |
| 依赖更新 | 按需 | pip install --upgrade {package}，更新后重跑验证 |

## 6. 排错手册

| 问题 | 可能原因 | 处理方式 |
|---|---|---|
| `ModuleNotFoundError` | venv 未创建或依赖缺失 | 创建 venv 并 `pip install` 缺失包 |
| VERIFY.ps1 hash 不匹配 | 文件修改后 MANIFEST 未更新 | 重新生成 MANIFEST.yaml |
| QCM-ALL FAIL | PYTHONPATH 未设置或路径转义错误 | qa_runner.py 已内置 PYTHONPATH 和路径修复 |
| PowerShell 中文乱码 | 默认 GBK 编码 | 设置 `$env:PYTHONUTF8='1'` 或使用 UTF8 编码调用 |
| Submodule 指针偏移 | 子模块有新 commit 未同步 | `git submodule update --remote` 后提交根指针 |
| 循环导入 (calculator) | qcm.core → calculator → qcm.config | calculator.py 保留模块级默认值，标注 config source |
| `ImportError: cannot import name 'AESGCM'` | 缺少 cryptography 包 | `pip install cryptography` |

## 7. 交接清单

- 交付包已移除本机绝对路径（使用 `project-root` 占位）。
- 交付包已移除个人密钥、token、账号密码（环境变量配置，不写入文件）。
- README 与四体系文档已按真实项目更新（基于 2026-05-28 全量验证结果）。
- 验证命令已在当前环境运行：`qa_runner.py validate` 结果 12 PASS / 1 FAIL / 1 WARN / 4 MANUAL。
- Git 仓库已推送至 GitHub：`https://github.com/letplaylimited-MARK/mother-delivery-package`（10 commits）。
- 已知风险和后续事项：
  - AKU-KNOWLEDGE-ATOM-SPEC.md 待建（知识原子进入知识库的正式规范）。
  - TRACEABILITY-MATRIX.md 仅模板无项目实例。
  - 02 通用知识库框架仍为模板态。
  - calculator.py/detector.py 因循环依赖保留硬编码值（config source 已标注）。
