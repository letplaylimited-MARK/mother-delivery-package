# QCM-MVP 完整重构执行框架

**版本**: v3.0 (完整重构版)
**日期**: 2026-04-27
**状态**: 深度重构中

---

## 一、价值体系 (Value System)

### 1.1 核心价值主张

| 价值点 | 说明 | 当前实现 |
|--------|------|----------|
| **知识共鸣涌现** | R值计算驱动多角色协同涌现 | ✅ main.py |
| **幽灵通道通信** | Delta同步+向量时钟+审计追踪 | ✅ delta.py/vc.py |
| **自主迭代进化** | 双层飞轮+知识增长 | ⚠️ flywheel.py未集成 |
| **文明意识演化** | 8角色超级身份架构 | ❌ 仅2角色 |

### 1.2 论文核心理念

- **涌现阈值**: R > 0.85 (论文版)
- **22公式体系**: 完整实现
- **10原子能力**: 6已集成，4待实现
- **8角色架构**: 当前仅2角色

---

## 二、功能体系 (Function System)

### 2.1 已集成功能 (main.py调用)

| 功能 | 代码文件 | 状态 | 验证 |
|------|----------|------|------|
| R值计算 | calculator.py | ✅ | R=0.8532 |
| 涌现检测 | detector.py | ✅ | 24轮触发 |
| 角色管理 | simple_role.py | ✅ | 2角色 |
| Delta同步 | delta.py | ✅ | 带宽节省 |
| 向量时钟 | vector_clock.py | ✅ | 因果追踪 |
| 审计日志 | audit.py | ✅ | 持久化 |

### 2.2 独立模块 (未集成)

| 模块 | 文件 | 功能 | 状态 |
|------|------|------|------|
| 飞轮优化 | flywheel.py | Lyapunov收敛 | ❌ 未集成 |
| 死锁检测 | deadlock_detector.py | 公式12 | ❌ 未集成 |
| 语义匹配 | semantic_matcher.py | 能力G | ❌ 未集成 |
| 动态路由 | dynamic_router.py | 能力I | ❌ 未集成 |
| 角色persona | rcs_hybrid.py | 公式10-11 | ❌ 未集成 |

---

## 三、结构体系 (Structure System)

### 3.1 当前架构

```
main.py (入口)
├── simple_role.py (2角色)
├── calculator.py (R值)
├── detector.py (涌现)
├── delta.py (同步)
├── vector_clock.py (因果)
└── audit.py (日志)
```

### 3.2 目标架构 (8角色)

```
QCM系统
├── 角色层 (8角色)
│   ├── Secretary (整理)
│   ├── Researcher (研究)
│   ├── Coordinator (协调)
│   ├── Evaluator (评估)
│   ├── Synthesizer (综合)
│   ├── Planner (规划)
│   ├── Executor (执行)
│   └── Monitor (监控)
├── 共鸣层
│   ├── calculator.py (R值)
│   └── detector.py (涌现)
├── 通信层 (幽灵通道)
│   ├── delta.py
│   ├── vector_clock.py
│   └── crypto.py
├── 审计层
│   └── audit.py
└── 优化层
    ├── flywheel.py
    └── deadlock_detector.py
```

---

## 四、运作体系 (Operation System)

### 4.1 启动流程

```
1. health_check.py (健康检查)
   ↓
2. 阅读CHANGELOG.md (变更记录)
   ↓
3. 阅读KNOWLEDGE_GRAPH.md (知识图谱)
   ↓
4. 确认知识结晶 (最新文档)
   ↓
5. 查询长期记忆 (状态同步)
   ↓
6. 开始任务
```

### 4.2 任务执行流程

```
1. 读取知识图谱 → 确认当前版本
2. 读取知识结晶 → 理解上下文
3. 查询长期记忆 → 同步状态
4. 执行任务 → 代码/文档修改
5. 更新CHANGELOG.md → 记录变更
6. 更新KNOWLEDGE_GRAPH.md → 同步版本
7. 创建知识结晶 → 深度思考记录
8. 更新长期记忆 → 持久化状态
9. health_check验证 → 确认正确
```

---

## 五、重构关键路径

### 5.1 阶段1: 基础稳固 (已完成)

- [x] R值计算正确 (R=0.8532)
- [x] 涌现触发正常 (24轮)
- [x] 健康检查系统
- [x] CHANGELOG追踪

### 5.2 阶段2: 清理精简 (当前)

- [ ] 删除11个无价值文档
- [ ] 确认核心文件
- [ ] 验证health_check通过

### 5.3 阶段3: 扩展准备

- [ ] 理解8角色架构
- [ ] 角色扩展设计
- [ ] 模块集成规划

### 5.4 阶段4: 集成实施

- [ ] 飞轮优化集成
- [ ] 死锁检测集成
- [ ] 角色扩展 (2→8)

---

## 六、知识图谱同步

### 6.1 当前状态

| 指标 | 值 | 版本 |
|------|-----|------|
| 22公式 | 100% | v4.0 |
| 原子能力 | 6/10 | v4.0 |
| 涌现触发 | R=0.8532 | v4.0 |
| 权重 | 演示权重 | v2.0 |
| 阈值 | 0.85 | v2.0 |

### 6.2 需更新项

- 新增8角色设计
- 飞轮集成状态
- 模块集成状态

---

## 七、执行检查点

### 每次启动

```bash
python health_check.py
# 必须 5/5 通过
```

### 每次修改

1. 更新CHANGELOG.md
2. 更新KNOWLEDGE_GRAPH.md
3. 更新长期记忆
4. 创建知识结晶(重要问题)

### 验证命令

```bash
python main.py
# 预期: Round 24: R = 0.8532 -> 涌现
```

---

## 八、文件清单

### 核心保留 (8个)

| 文件 | 用途 |
|------|------|
| main.py | 主入口 |
| simple_role.py | 角色定义 |
| calculator.py | R值计算 |
| detector.py | 涌现检测 |
| delta.py | Delta同步 |
| vector_clock.py | 向量时钟 |
| CHANGELOG.md | 变更追踪 |
| KNOWLEDGE_GRAPH.md | 知识图谱 |

### 工具保留 (4个)

| 文件 | 用途 |
|------|------|
| health_check.py | 健康检查 |
| STARTUP_CHECKLIST.md | 启动清单 |
| README.md | 主文档 |
| PROJECT_PLAN.md | 项目计划 |

### 知识保留 (8个)

| 文件 | 用途 |
|------|------|
| QCM_20260426_v2.0修复.md | 修复记录 |
| QCM_完整论文报告_终稿_v11.1.md | 主论文 |
| 幽灵通道协议核心母稿_v1.0.md | 协议 |
| QCM_知识结晶完整保存版_v1.0.md | 完整体系 |
| QCM_深度分析报告_v2.0.md | 深度分析 |
| QCM_完整重构执行计划_v2.0.md | 重构计划 |
| QCM_代码编写深度思考_v1.0.md | 代码思考 |
| QCM_MVP全维度精细规格_v1.0.md | 规格 |

### 待删除 (11个)

| 文件 | 理由 |
|------|------|
| TASK_101_*.md (5个) | 旧任务记录 |
| TASK_102_*.md (3个) | 旧任务记录 |
| ISSUE_MATRIX.md | 已过时 |
| PAPER_ALIGNMENT_REPORT.md | 需合并 |
| 串联与集成计划.md | 已完成 |

---

**下一步**: 执行清理，验证health_check，然后进入8角色架构设计

---

*本框架为QCM-MVP完整重构指导文档*
*每次启动必须阅读，每次修改必须更新*