# QCM-MVP-Emergence 快速启动指南

**版本**: v1.0 → **v6.3 (最新)**  
**日期**: 2026-04-20 (原始) → **2026-05-24 (更新)**
> ⚠️ **本文檔為 v1.0 原始版，已由 `README.md` v6.3 和 `PROJECT_HANDOFF-QCM.md` 取代。**
> 以下為保留的歷史內容，新用戶請直接閱讀 `README.md`。

> 2026-05-31 審計補充：當前可執行入口請以 `README.md` / `PROJECT_HANDOFF-QCM.md` / `SUBSYSTEM-CRYSTAL-P04-QCM-AND-QCM-SKILL.md` 為準。CLI 輪次參數為 `--max-rounds`，不是舊版 `--rounds`。

```bash
python "02-代码编写/main.py"
python "02-代码编写/main_complete.py"
python -m qcm.main --mode research --seed 42 --max-rounds 22
python qa_runner.py validate --scope P04_QCM
```

---

## 一句话说明

用最小可运行代码，证明"幽灵通道 + 共鸣公式 = 涌现发生"

---

## 核心公式

论文公式：

$$R = 0.25 \cdot K_{sim} + 0.35 \cdot C_{comp} + 0.20 \cdot I_{freq} - 0.20 \cdot E_{divergence}$$

当前 MVP 演示公式：

$$R = 0.30 \cdot K_{sim} + 0.40 \cdot C_{comp} + 0.25 \cdot I_{freq} - 0.15 \cdot E_{divergence}$$

**论文阈值**：`R > 0.85`  
**当前 MVP 阈值**：`R > 0.75`

---

## 快速开始

### 运行演示

```bash
cd "<QCM-MVP-Emergence根目录>\02-代码编写"
python main.py
```

### 预期输出

```
Round  1: R = 0.52~0.59
...
Round 20: R = 0.7545
🎉 涌现发生！
```

---

## 项目结构

```
QCM-MVP-Emergence/
├── 00-知识结晶/          # 核心知识文档
├── 01-幽灵通道SDK/       # SDK参考
├── 02-代码编写/          # MVP代码（已实现）
│   ├── simple_role.py   # 角色定义
│   ├── delta.py         # 增量同步
│   ├── vector_clock.py  # 因果排序
│   ├── calculator.py   # R值计算
│   ├── detector.py      # 涌现检测
│   └── main.py          # 演示入口
├── 03-测试验证/
├── 04-运行结果/
└── 05-参考资料/
```

---

## 当前可用能力

1. `main.py` 可直接运行
2. `delta.py` 已集成
3. `vector_clock.py` 已集成，且 TASK-103 已完成因果追踪增强
4. `calculator.py` / `detector.py` 已集成
5. `audit.py` 已通过 TASK-104 接入主流程

---

## 验收标准

| 级别 | 标准 |
|------|------|
| 最小 | `python main.py` 不报错 |
| 基础 | R值在[0,1]范围 |
| 核心 | 第20轮左右触发涌现 |
| 当前目标 | R > 0.75，输出"🎉" |
| 论文目标 | R > 0.85 |

---

## 参考文档

- `00-知识结晶/QCM_MVP深度优化规划_v2.0.md` - 完整规划
- `00-知识结晶/QCM_知识结晶完整保存版_v1.0.md` - 22公式体系
- `00-知识结晶/QCM_MVP全维度精细规格_v1.0.md` - 技术规格
- `00-知识结晶/QCM_MVP深度对齐执行规划_v1.0.md` - 当前执行策略
- `02-代码编写/KNOWLEDGE_GRAPH.md` - 当前代码知识图谱
- `02-代码编写/ISSUE_MATRIX.md` - 当前问题矩阵

---

*快速启动指南 - 详细规划见知识结晶文件夹*
