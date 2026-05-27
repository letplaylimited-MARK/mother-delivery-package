# Phase 1: 文件夹清理与重组

## 1.1 已删除文件

| 文件 | 理由 |
|------|------|
| main.py.backup_v1 | 旧备份 |
| main.py.backup_20260418 | 旧备份 |
| main_v2.py | 重复版本 |
| verify_*.py (4个) | 临时验证 |
| trace_r.py | 临时调试 |
| bug_check.py | 临时调试 |
| FILE_REORGANIZATION.md | 旧文档 |
| DELIVERY_DEMO_GUIDE.md | 旧文档 |
| FULL_PAPER_INTEGRATION_PLAN.md | 旧文档 |
| I01_EMBEDDING_INTEGRATION_PLAN.md | 旧文档 |
| STREAMLIT_VERIFICATION.md | 旧文档 |
| MVP_PAPER_DIFF_SUMMARY.md | 旧文档 |
| P2_DEEP_CODE_REVIEW.md | 旧文档 |
| DEEP_ALIGNMENT_ANALYSIS.md | 旧文档 |
| EXECUTION_PLAN.md | 旧文档 |
| TEMPLATE_RECORD.md | 旧文档 |
| KNOWLEDGE_GRAPH.md (02-代码编写) | 已移到根目录 |

## 1.2 当前结构

```
QCM-MVP-Emergence/
├── CHANGELOG.md              # 变更追踪 (v3.0)
├── health_check.py            # 健康检查 (v2.0)
├── KNOWLEDGE_GRAPH.md       # 知识图谱 (v4.0)
├── RECONSTRUCTION_FRAMEWORK.md # 重构框架 (v3.0)
├── STARTUP_CHECKLIST.md      # 启动检查清单
├── README.md              # 主文档
├── PROJECT_PLAN.md        # 项目计划
├── QUICKSTART.md          # 快速启动
├── 00-知识结晶/           # 13个知识文档
├── 01-幽灵通道SDK/        # SDK代码
├── 02-代码编写/           # 核心代码
├── 03-测试验证/          # 测试目录
├── 04-运行结果/          # 运行结果
└── 05-参考资料/          # 论文/参考
```

## 1.3 health_check验证

```
[CHECK] CHANGELOG...  OK
[CHECK] KNOWLEDGE_GRAPH...  OK
[CHECK] simple_role version...  OK
[CHECK] calculator weights...  OK
[CHECK] detector threshold...  OK
Result: 5/5 OK
Status: READY
```

---

# Phase 2: AI角色团队沙盘推演

## 2.1 角色定义

### 角色1: 系统架构师 (Architect)
- **职责**: 设计系统架构和扩展方案
- **技能**: 架构设计、模块划分、接口定义
- **视角**: 整体视角

### 角色2: 集成专家 (Integrator)
- **职责**: 模块集成和依赖管理
- **技能**: 代码集成、API对接、版本兼容
- **视角**: 连接视角

### 角色3: 优化专家 (Optimizer)
- **职责**: 性能和效率优化
- **技能**: 算法优化、资源管理、缓存策略
- **视角**: 效率视角

### 角色4: 验证专家 (Validator)
- **职责**: 质量验证和测试
- **技能**: 测试设计、边界检查、回归测试
- **视角**: 质量视角

### 角色5: 规划专家 (Planner)
- **职责**: 阶段规划和里程碑
- **技能**: 任务分解、优先级排序、风险评估
- **视角**: 时间视角

---

## 2.2 沙盘推演主题

### 主题1: 8角色架构设计
- 如何从2角色扩展到8角色？
- 角色间如何通信？
- R值如何扩展计算？

### 主题2: 飞轮集成
- flywheel.py如何集成到main.py？
- 触发条件是什么？
- 收敛判断标准？

### 主题3: 死锁检测集成
- deadlock_detector.py如何集成？
- 预警机制如何工作？
- 阈值如何设置？

### 主题4: 下一步优先级
- 应该先做什么？
- 风险是什么？
- 里程碑如何设置？

---

## 2.3 飞轮模式规则

1. **每轮**: 每个角色提出一个观点/建议
2. **共识**: 多轮讨论后达成的共识
3. **迭代**: 3轮迭代，每轮20次思考
4. **决策**: 最终决策记录

---

*本文件为AI角色团队沙盘推演记录*
*更新日期: 2026-04-27*