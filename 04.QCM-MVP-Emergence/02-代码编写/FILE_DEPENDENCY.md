# 02-代码编写 目录文件依赖分析

## 分析日期: 2026-04-27

---

## 1. 核心依赖关系 (main.py调用链)

```
main.py
├── simple_role.py       ← 必需 (角色定义)
├── delta.py           ← 必需 (Delta同步)
├── vector_clock.py    ← 必需 (向量时钟)
├── calculator.py     ← 必需 (R值计算)
├── detector.py       ← 必需 (涌现检测)
└── qcm_emergence.ghost_channel.audit ← 可选
```

**必需文件 (7个)**:
- main.py
- simple_role.py
- delta.py
- vector_clock.py
- calculator.py
- detector.py
- knowledge_manager.py (可选)

---

## 2. 独立模块 (未集成，main.py不调用)

| 文件 | 状态 | 说明 |
|------|------|------|
| deadlock_detector.py | 独立 | 未集成，公式12 |
| flywheel.py | 独立 | 未集成，公式16-18 |
| knowledge_growth.py | 独立 | 未集成，公式19-20 |
| sandbox.py | 独立 | 未集成，公式14-15 |
| semantic_matcher.py | 独立 | 能力G，未集成 |
| dynamic_router.py | 独立 | 能力I，未集成 |
| neural_router.py | 独立 | 公式21，未集成 |
| pareto_cost.py | 独立 | 公式22，未集成 |
| dynamic_weight.py | 独立 | 公式7，未集成 |
| predictive_sync.py | 独立 | 能力H，未集成 |
| rcs_hybrid.py | 独立 | 公式10-11，未集成 |
| mahalanobis_distance.py | 独立 | 公式8，未集成 |
| epr_entanglement.py | 独立 | 公式6，未集成 |
| zk_proof.py | 独立 | 能力J，未集成 |

---

## 3. 重复/冗余文件

### 3.1 qcm_emergence包 (重复版本)

| 文件 | 主版本 | 关系 |
|------|-------|------|
| qcm_emergence/simple_role.py | simple_role.py | 重复 |
| qcm_emergence/resonance/calculator.py | calculator.py | 重复 |
| qcm_emergence/resonance/detector.py | detector.py | 重复 |
| qcm_emergence/ghost_channel/* | delta.py/vc.py | 重复/扩展 |

**建议**: qcm_emergence包为SDK包装，可保留但非必需

### 3.2 streamlit_app.py

- 可选依赖，不影响主流程
- 需要: streamlit, numpy, matplotlib

---

## 4. 文件分类建议

### 4.1 核心保留 (7个)

```
main.py              主入口
simple_role.py      角色定义
delta.py            Delta同步
vector_clock.py     向量时钟
calculator.py       R值计算
detector.py         涌现检测
knowledge_manager.py 知识管理 (可选)
```

### 4.2 独立模块 (14个)

```
deadlock_detector.py  死锁检测
flywheel.py         飞轮优化
knowledge_growth.py 知识增长
sandbox.py         三层沙盘
semantic_matcher.py 语义匹配
dynamic_router.py   动态路由
neural_router.py   神经路由
pareto_cost.py     帕累托成本
dynamic_weight.py  动态权重
predictive_sync.py  预测同步
rcs_hybrid.py     角色混合
mahalanobis_distance.py 马氏距离
epr_entanglement.py EPR纠缠
zk_proof.py        ZK证明
```

### 4.3 可选保留 (1个)

```
streamlit_app.py     可视化
```

### 4.4 可删除/归档 (qcm_emergence包)

```
qcm_emergence/      可移至01-幽灵通道SDK/
```

---

## 5. 依赖检查

```bash
python main.py
# 输出: R=0.8532 @ 24轮
```

---

## 6. 结论

| 类别 | 数量 | 状态 |
|------|------|------|
| 核心代码 | 7 | ✅ 必需 |
| 独立模块 | 14 | ⏸ 待集成 |
| 可视化 | 1 | 可选 |
| qcm_emergence | 9 | 可归档 |

**建议**: 
1. 核心7个文件保持不变
2. 独立14个模块保持不变(未来集成用)
3. qcm_emergence包可移至SDK目录

---

*更新日期: 2026-04-27*