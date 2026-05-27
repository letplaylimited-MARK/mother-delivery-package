# QCM 22公式系统架构

> **v6.3 更新**: 以下所有 22 条公式均已实现并通过 63/63 测试。
> 参见 `PROJECT_HANDOFF-QCM.md` 和 `README.md` 获取最新状态。
> 原始计划（Phase 1-4）已全部完成。

## 核心公式体系 (22 formulas)

### 第一层: 基础度量 (Formulas 1-5)
```
Formula 1: R = w1*K + w2*C + w3*I - w4*E  [共鸣能量核心]
Formula 2: K_sim = cos(e_i, e_j)              [知识相似度]
Formula 3: C_comp = 1 - Jaccard(S_i, S_j)      [技能互补性]
Formula 4: I_freq = F/(F+F0) * exp(-λΔt)       [交互频率]
Formula 5: E_div = KL(P_i||P_j) + KL(P_j||P_i) [专业分歧]
```

### 第二层: 动态调整 (Formulas 6-9)
```
Formula 6: E(A,B) = sqrt(1-Tr(...)) + λ⟨[A,B]⟩  [量子纠缠类比]
Formula 7: w_i,t = w_i,t-1 + λ(R - R_target)    [动态权重]
Formula 8: d_M = sqrt((x-y)T Σ^-1 (x-y))       [马氏距离]
Formula 9: L = max(0, d_M - m_pos) + ...      [度量学习]
```

### 第三层: 一致性与死锁 (Formulas 10-13)
```
Formula 10: BLEU_role = BP * exp(Σwn log pn + βI_persona)  [角色一致性]
Formula 11: I_persona = log(P(w|S))/(|S|+ε)    [人格指标]
Formula 12: Deadlock = I(α1I[N<ηN] + α2I[G>ηG] + ...) [死锁检测]
Formula 13: S_soft = 0.3(1-N) + 0.35*G + ...  [软死锁分数]
```

### 第四层: 飞轮与增长 (Formulas 14-20)
```
Formula 14: df_k/dt = λ(1-f_k/fmax)I[success] - μf_kI[failure]  [复杂度]
Formula 15: SRS = (1/T)∫ exp(-(f-f_target)²/2σ²) dt  [成功率]
Formula 16: dθ/dt = α∇L - βθ + γε  [飞轮梯度]
Formula 17: α(t) = α_init * 1/(1+γt^κ) * exp(-λvar) [学习率]
Formula 18: A(t) = A0 * (1 + η*t/t_ref)^ζ  [飞轮累积]
Formula 19: dK/dt = η * E^(1/3) * S^0.7  [知识增长]
Formula 20: K(t) = K0 * exp[η*s^0.7*(t^4/3)] [知识累积]
```

### 第五层: 决策与优化 (Formulas 21-22)
```
Formula 21: D(input) = argmax P(r|features)  [决策类型选择]
Formula 22: C(option) = α*R_cost + β*Risk + γ*Opp_loss [成本优化]
```

---

## 公式依赖关系图

```
Layer 1 (基础度量):
  Formula 2 ──┐
  Formula 3 ──┼──> Formula 1 (R)
  Formula 4 ──┤
  Formula 5 ──┘

Layer 2 (动态调整):
  Formula 1 ──> Formula 7 (权重调整)
  Formula 2 ──> Formula 8 (马氏距离)
  Formula 8 ──> Formula 9 (度量学习)

Layer 3 (一致性):
  Formula 1 ──> Formula 10 (角色一致性)
  Formula 10 ─> Formula 11 (人格指标)
  Formula 1 ──> Formula 12 (死锁检测)
  Formula 12 ─> Formula 13 (软死锁)

Layer 4 (飞轮):
  Formula 1 ──> Formula 14 (复杂度)
  Formula 14 ──> Formula 15 (成功率)
  Formula 15 ──> Formula 16 (梯度)
  Formula 16 ──> Formula 17 (学习率)
  Formula 17 ──> Formula 18 (累积)
  Formula 18 ──> Formula 19 (知识增长)
  Formula 19 ──> Formula 20 (知识累积)

Layer 5 (决策):
  Formula 1 ──┐
  Formula 13 ──┼──> Formula 21 (决策)
  Formula 20 ──┘
              │
              └──> Formula 22 (成本优化)
```

---

## 8角色架构与公式映射

| 角色 | 核心公式 | 主要贡献 |
|------|---------|---------|
| Secretary | F1, F3 | C_comp (技能整理) |
| Researcher | F1, F2, F8 | K_sim (知识探索) |
| Coordinator | F4, F7 | I_freq, 动态权重 |
| Evaluator | F10, F11 | 角色一致性 |
| Synthesizer | F19, F20 | 知识增长 |
| Planner | F21, F22 | 决策与成本 |
| Executor | F14, F15 | 复杂度与成功率 |
| Monitor | F12, F13 | 死锁检测 |

---

## 当前MVP实现 vs 完整论文体系 (v6.3)

### 已实现 (全部完成 ✅)
| 层级 | 公式 | 实现位置 | 状态 |
|------|------|----------|------|
| L1 | F1-F5 共鸣核心 | `qcm/core/` | ✅ 管线集成 |
| L2 | F6 EPR纠缠 / F7 动态权重 | `qcm/enhanced/` | ✅ 管线集成 |
| L3 | F8-F9 马氏距离 / F10-F11 RCS / F12-F13 死锁 | `qcm/enhanced/` | ✅ 管线集成 |
| L4 | F14-F15 沙盘 / F16-F18 飞轮 / F19-F20 知识增长 | `qcm/evolution/` | ✅ 管线集成 |
| L5 | F21 神经路由 / F22 Pareto成本 | `qcm/decision/` | ✅ (feature flag) |

### 论文扩展模块 (Phase 6)
| 论文章节 | 模块 | 功能 |
|----------|------|------|
| §3.2 角色身份 | `qcm/roles/` | 8角色模板 + weighted consensus + safety veto |
| §4 协作协议 | `qcm/collaboration/` | 5阶段会议 + VoteMode + 死锁检测 + AuditLog |
| §7 沙盒隔离 | `qcm/sandbox/` | 3层沙盘 + SRS评分 + CBP调度 |
| §8 飞轮优化 | `qcm/flywheel/` | 内外循环 + 能量函数 + Lyapunov稳定性 |
| §9 召唤匹配 | `qcm/summoning/` | TF-IDF特征 + SkillMatch + 动态惩罚 |

### 8角色支持 ✅
8个角色模板（Secretary, Researcher, Coordinator, Evaluator, Synthesizer, Planner, Executor, Monitor）+ 动态召唤（DynamicRoleRegistry）已实现。

---

## 架构设计原则

1. **层层递进**: 每层公式依赖前一层的输出
2. **闭环反馈**: R值影响权重调整(F7),权重影响飞轮(F16-F20)
3. **动态演化**: 知识累积(K)随时间增长,驱动涌现
4. **8角色分工**: 每个角色负责特定公式子集

---

## 完成状况 (v6.3)

所有 Phase 1-4 已全部完成。参见 `PROJECT_HANDOFF-QCM.md` 获取完整交付摘要。

### 验证结果
| 测试套件 | 通过率 |
|----------|--------|
| test_qcm_all.py | 25/25 ✅ |
| test_roles.py | 6/6 ✅ |
| test_collaboration.py | 7/7 ✅ |
| test_sandbox.py | 8/8 ✅ |
| test_flywheel.py | 11/11 ✅ |
| test_summoning.py | 6/6 ✅ |
| **合计** | **63/63 ALL PASS** ✅ |

---

**文件**: QCM_完整论文报告_终稿_v11.1.md
**参考章节**: 第2章 (数学理论基础), 包含22个公式完整推导