# AKU 知识原子规范 v1.0

> **用途**：定义"知识原子（AKU = Atomic Knowledge Unit）"的格式、分类、存储位置、验证方式和与 03/05 知识库的接口契约。
> **来源**：元智核系统超级提示词（转译后吸收），映射至 03 知识图谱、05 BRAIN-KB、MISSION-MEMORY。
> **状态**：初版，待在真实项目中验证并迭代。

---

## 1. 核心定义

**知识原子（AKU）** = 一条可独立验证、可溯源、可连接的知识记录。

三条红线：
- 必须有来源（文件名 / URL / 对话 ID）
- 必须有置信度（High / Medium / Low，或 0.0–1.0 数值）
- 必须可重新验证（不能只有结论，没有证据路径）

---

## 2. 分类体系

| 类型 | 说明 | 典型位置 |
|---|---|---|
| **FACT** | 可验证的客观事实 | 03-wiki/sources/, 05-BRAIN-KB/knowledge/ |
| **INFERENCE** | 基于事实的推理结论 | MISSION-MEMORY.md, HANDOFF.md |
| **DECISION** | 已执行的决策记录 | DECISION-LOG.md, ADR-*.md |
| **GATE** | 阶段门判定结果 | qa_runner.py validate 输出 |
| **RISK** | 已识别的风险项 | HANDOFF.md §风险提示 |

---

## 3. 格式规范

### 3.1 最小 AKU 模板（Markdown Frontmatter）

```markdown
---
aku_id: AKU-2026-0529-001
type: FACT
source: 00/13-源提示词吸收与演化/SUPER-PROMPT-ATOMIC-RESEARCH-REVIEW.md#102
confidence: High
verified: true
verified_by: qa_runner.py
verified_at: 2026-05-29
links: [AKU-2026-0529-002]
---

# AKU 正文

26/26 原子机制已在母包中落地（SUPER-PROMPT-ATOMIC-RESEARCH-REVIEW.md 第4节）。
```

### 3.2 置信度规范

| 等级 | 含义 | 使用条件 |
|---|---|---|
| **High** | 有文件/测试/日志证据 | 必须通过 qa_runner.py 或 TEST 条目验证 |
| **Medium** | 有推理链但缺少直接证据 | 必须在 `links` 中指向至少一个 High 级 AKU |
| **Low** | 假设/待验证 | 必须标记 `verified: false`，并在 `links` 中说明验证计划 |

**禁止**：
- `confidence: High` 但 `verified: false`
- 无 `source` 字段的 AKU（"常识"也必须标注来源或标记为 INFERENCE）

---

## 4. 存储位置与接口契约

### 4.1 与 03 知识库（knowledge-base-manager）的契约

| 操作 | 接口 | 说明 |
|---|---|---|
| 写入 AKU | `03/01-raw/` → 触发 Ingest → `03/03-wiki/sources/` | 符合 03 的 Ingest 工作流 |
| 查询 AKU | `03/03-wiki/index.md` + concepts/ | 通过知识图谱索引检索 |
| 验证 AKU | 运行 `03/scripts/test.ps1` | 103 测试全 PASS 视为知识库级验证通过 |

### 4.2 与 05 Q-SpecTrum BRAIN-KB 的契约

| 操作 | 接口 | 说明 |
|---|---|---|
| 写入 AKU | `05/BRAIN-KB/knowledge/` | 直接写入，由 05 的 INDEX.md 索引 |
| 查询 AKU | `05/BRAIN-KB/INDEX.md` | 总索引文件 |
| 向量检索 | `05/BRAIN-KB/.chroma_db/` | ChromaDB 向量库，由 05 的 MCP 接口查询 |

### 4.3 与 MISSION-MEMORY 的契约

- 每次唤醒时，MISSION-MEMORY.md 读取最近 5 条 High 置信度 AKU
- AKU 的 `links` 字段用于构建唤醒上下文（替代"假装长期记忆"）
- 写入 MISSION-MEMORY.md 的 AKU 必须带 `source` 文件路径

---

## 5. 验证方式

### 5.1 单条 AKU 验证

| 检查项 | 工具 | PASS 条件 |
|---|---|---|
| source 存在 | Bash `test -f <source>` | 文件存在或可访问 URL |
| confidence 与 verified 一致 | Read + 人工审查 | 不出现 High + false |
| links 指向有效 AKU | Grep `aku_id:` | 所有 link 目标存在 |
| 无幻觉结论 | 对比 source 原文 | 结论可在 source 中找到依据 |

### 5.2 批量 AKU 验证（接入 qa_runner.py）

在 `qa_runner.py` 中新增子命令 `validate_aku`：

```
python qa_runner.py validate_aku --root <project-root>
```

检查范围：
- 扫描所有 `**/AKU-*.md` 和 Markdown 文件中的 `aku_id:` frontmatter
- 输出：PASS / FAIL / WARN（缺失 source / 置信度矛盾 / 断链）

---

## 6. 示例 AKU

### 示例 1：FACT 类型（已验证）

```markdown
---
aku_id: AKU-2026-0529-002
type: FACT
source: 00/08-AI角色团队沙盘/README.md#角色定义
confidence: High
verified: true
verified_by: 人工审查
verified_at: 2026-05-29
links: [AKU-2026-0529-001]
---

# QCM 沙盘角色定义

QCM 定义 12 个角色（产品/架构/开发者/测试/运维/安全/数据/UX/业务/法律/竞品/终验），
用于多角色审查机制（SUPER-PROMPT-ATOMIC-RESEARCH-REVIEW.md 第3节）。
```

### 示例 2：DECISION 类型（带 ADR 链接）

```markdown
---
aku_id: AKU-2026-0529-003
type: DECISION
source: 00/07-版本与状态管理/DECISION-LOG.md#DEC-001
confidence: High
verified: true
verified_by: DECISION-LOG
verified_at: 2026-05-28
links: [AKU-2026-0529-001]
---

# 决策：QCM Phase 2 采用 config-driven 迁移

采纳方案：扩展 qcm/config.py，新增 paper_params 段，12/14 模块完成迁移（60 个常量）。
拒绝方案：直接全局替换硬编码值（无法追溯参数来源）。
```

---

## 7. 与源提示词的映射关系

| 元智核原始概念 | 本规范对应 | 吸收等级 |
|---|---|---|
| AKUv2.0 知识原子元数据 | §3 格式规范 + §4 存储契约 | A-直接吸收 |
| 双螺旋知识结构 | §4.1 + §4.2（知识图谱 + BRAIN-KB 双存） | A-直接吸收 |
| 知识结晶（推理链） | §2 INFERENCE 类型 + links 字段 | A-直接吸收 |
| "每次成功 AKU 置信度 +0.1" | ❌ 拒绝（伪量化） | D-拒绝吸收 |
| 768 维向量强制 | ⚠️ 改为可选（由 05 BRAIN-KB 决定维度） | B-转译后吸收 |

---

## 8. 待完善

- [ ] 在 `qa_runner.py` 中实装 `validate_aku` 子命令
- [ ] 为 00-13 目录下所有研究文档补充 AKU frontmatter
- [ ] 建立 AKU 数量看板（MISSION-MEMORY.md 中展示 High 级 AKU 计数）
- [ ] 定义 AKU 过期策略（超过 30 天未 re-verified 的 AKU 标记为 Stale）

---

*本规范本身就是一个 AKU（type: FACT，source: 本文档）。*
*版本变更记录在 00/07-版本与状态管理/CHANGELOG.md。*
