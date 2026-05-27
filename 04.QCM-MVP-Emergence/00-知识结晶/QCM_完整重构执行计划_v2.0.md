# QCM完整重构执行计划

**日期**: 2026-04-26  
**版本**: v2.0  
**重构目标**: 论文完整对齐（0.85阈值、8角色、22公式集成）

---

## 一、重构范围

### 1.1 核心修改项

| # | 修改项 | 当前值 | 目标值 | 风险 |
|---|--------|--------|--------|------|
| 1 | EmergenceDetector阈值 | 0.75 | **0.85** | 高 |
| 2 | ResonanceCalculator权重 | 0.30/0.40/0.25/0.15 | **0.25/0.35/0.20/0.20** | 高 |
| 3 | 角色系统 | 2角色 | **8角色** | 高 |
| 4 | 涌现触发轮次 | 20轮 | **5-10轮** | 高 |
| 5 | 公式集成 | 6/10 | **22公式** | 中 |

### 1.2 风险缓解策略

| 策略 | 说明 |
|------|------|
| 备份 | 创建main.py.backup_v1 (保留当前稳定版本) |
| 验证 | 每个Task执行后运行测试 |
| 回滚 | 如果失败可回退到v1 |

---

## 二、Task分解

### Task 1: 备份与准备工作

**目标**: 备份当前版本，创建新目录

**步骤**:
- [ ] 1.1 复制main.py → main.py.backup_v1
- [ ] 1.2 创建目录qcm_emergence_v2/
- [ ] 1.3 运行main.py验证基线可用

**验证**: `python main.py.backup_v1` 正常输出涌现

---

### Task 2: 修改detector.py阈值

**目标**: 论文对齐0.85阈值

**步骤**:
- [ ] 2.1 修改THRESHOLD_DEEP = 0.85
- [ ] 2.2 修改等级定义
- [ ] 2.3 运行验证

**验证**: `python -c "from detector import EmergenceDetector; d=EmergenceDetector(); print(d.THRESHOLD_DEEP)"` 输出0.85

---

### Task 3: 修改calculator.py权重

**目标**: 论文权重对齐

**步骤**:
- [ ] 3.1 修改W_K=0.25, W_C=0.35, W_I=0.20, W_E=0.20
- [ ] 3.2 验证权重和=1.0

**验证**: `python -c "from calculator import ResonanceCalculator; c=ResonanceCalculator(); print(c.W_K+c.W_C+c.W_I+c.W_E)"` 输出1.0

---

### Task 4: 修改simple_role.py角色系统

**目标**: 添加8角色支持

**步骤**:
- [ ] 4.1 创建Role基类
- [ ] 4.2 添加8个角色定义
- [ ] 4.3 创建角色管理器

**验证**: 导入8角色类成功

---

### Task 5: 创建新主入口emergence.py

**目标**: 新主引擎（论文对齐）

**步骤**:
- [ ] 5.1 创建EmergenceEngine类
- [ ] 5.2 集成飞轮优化
- [ ] 5.3 集成角色管理

**验证**: 运行5轮触发涌现

---

### Task 6: 验证测试

**步骤**:
- [ ] 6.1 运行main.py对比
- [ ] 6.2 运行emergence.py对比
- [ ] 6.3 记录R值差异

---

### Task 7: 更新文档

**步骤**:
- [ ] 7.1 更新PAPER_ALIGNMENT_REPORT.md
- [ ] 7.2 更新KNOWLEDGE_GRAPH.md
- [ ] 7.3 创建重构记录

---

## 三、执行约束

### 安全规则
- 每个Task后必须运行验证
- 失败立即停止并回滚
- 保持backup版本可用

### 验证标准
- R值在5-10轮达到0.85
- 涌现触发在预期轮次内
- 8角色可正常协作

---

## 四、关键代码位置

| 文件 | 行号 | 修改内容 |
|------|-----|----------|
| detector.py | 13 | THRESHOLD_DEEP |
| calculator.py | 12-15 | W_K/W_C/W_I/W_E |
| simple_role.py | 6-90 | 角色系统 |
| main.py | 1-415 | 完整重写 |

---

**执行原则**: 宁可慢，不要错。每个Task验证后再继续。