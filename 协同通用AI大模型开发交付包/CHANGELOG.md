# Changelog

> 格式参考 Keep a Changelog (keepachangelog.com)。
> 本文件记录母交付包的重要变更。

## [2026-05-28] — Session 3+: Phase 1 验证修复 + Phase 2 QCM 迁移 + 交付包填充

### Added
- Python venv 环境创建，6 核心依赖安装（cryptography, Flask, numpy, chromadb, pytest, pytest-asyncio）
- `qa_runner.py`: VENV_PYTHON 自动路由（`_reroute_python()`）、`run_cmd_raw()` 自定义 PYTHONPATH
- `qcm/config.py`: `paper_params` 段（14 模块所有论文校准参数）、`get_param()` 便捷方法
- `05/_HANDOFF/`: STATUS.md、CRITICAL-REMINDERS.md、MEMORY-INDEX.md
- `协同通用AI大模型开发交付包/AI_PROJECT_CONTEXT.md`: 交付版项目上下文
- `协同通用AI大模型开发交付包/HANDOFF.md`: 交接文档
- `协同通用AI大模型开发交付包/CHANGELOG.md`: 本文件
- `协同通用AI大模型开发交付包/TRACEABILITY-MATRIX.md`: 追踪矩阵
- `协同通用AI大模型开发交付包/VALIDATION_REPORT.md`: 验证报告
- 迁移脚本 `04/migrate_phase2.py`（可复用）

### Changed
- `qa_runner.py`: PowerShell UTF8 编码修复、QCM 测试路径修复（`\\`→`/`）、PYTHONPATH 设置
- `01/MANIFEST.yaml`: 重新生成（299 文件，排除 .pytest_cache/__pycache__）
- `04/` 12 个公式模块：60 个类常量迁移为 `_cfg.get_param()` config lookup
- `04/calculator.py` + `04/detector.py`: 因循环依赖保留硬编码但添加 config source 注释
- `.gitignore`: 补充 `.mypy_cache/` 和 `chroma_db/`

### Fixed
- VAL-01-GHOST-VERIFY: MANIFEST hash 不匹配（重新生成 + 排除 cache）
- VAL-01-SDK-TESTS: 0 tests（PYTHONPATH + cryptography 安装）
- VAL-03-INSTALL: Flask 依赖缺失（venv 安装）
- VAL-04-QCM-ALL: 中文路径转义 + PYTHONPATH 缺失
- VAL-05-INTEGRATION: chromadb 缺失 + _HANDOFF 目录缺失
- VAL-USER-PACK-DELIVERY-STRICT: 四体系模板→实际内容 + 5 个缺失文件创建

## [2026-05-28] — Session 2: 推送就绪 + 深度记忆

### Added
- GitHub 根仓库创建（letplaylimited-MARK/mother-delivery-package）
- 03 submodule push (e1b8318)
- 05 submodule push (c6deb02)
- 根仓库 submodule 指针更新 commit (05a8147)
- MEMORY.md 深度重构（5 大板块 + 量化统计）
- MOTHER-PACK-ACTIVATION-GUIDE.md 权威启动协议

### Fixed
- 05 Q-SpecTrum: Markdown fence 不平衡修复
- Git submodule 指针同步

## [2026-05-27-28] — Session 1: 项目审计与基线建立

### Added
- 项目全量扫描和基线建立
- 七子系统文件统计和 Git 状态确认
- qa_runner.py 首次运行和 18 条验证基线记录
- 00/validate_consistency.py 10 维一致性检查首次运行

### Discovered
- 6 个 FAIL（VAL-01/03/04/05 系列 + STRICT）
- Git remote 未配置
- Submodule 指针偏移
