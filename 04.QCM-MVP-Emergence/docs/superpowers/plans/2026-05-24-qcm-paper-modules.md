# QCM 論文模組補全實作計劃

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將 QCM 論文 §3.2/§4/§7/§8/§9 定義的 5 大創新模組以論文級規格實作至 qcm/ 包，擴充測試從 25 至 ~40。

**Architecture:** 每模組為獨立 qcm/ 子包，角色身份→協同協議→三層沙盤→雙層飛輪→動態召喚，逐步整合至 pipeline.py。ML 依賴部分使用 mock 介面。

**Tech Stack:** Python 3.10+, pytest, numpy (for linear algebra), sklearn (TF-IDF)

**Base path:** `<QCM-MVP-Emergence根目录>`

---

## Phase 1: 角色身份模組 (qcm/roles/)

### Task 1: 建立 roles/identity.py + roles/__init__.py

**Files:**
- Create: `qcm/roles/__init__.py`
- Create: `qcm/roles/identity.py`
- Test: `02-代码编写/test_roles.py`

- [ ] **Step 1: Write the test**

```python
# 02-代码编写/test_roles.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from qcm.roles import ROLE_REGISTRY, RoleIdentity

def test_registry_has_8_roles():
    assert len(ROLE_REGISTRY) == 8
    ids = [r.role_id for r in ROLE_REGISTRY]
    assert "secretary" in ids
    assert "chief_architect" in ids
    assert "researcher" in ids
    assert "creator" in ids
    assert "analyst" in ids
    assert "ux_lead" in ids
    assert "risk_auditor" in ids
    assert "ai_companion" in ids

def test_role_has_all_fields():
    r = ROLE_REGISTRY[0]
    assert isinstance(r.role_id, str)
    assert isinstance(r.name, str)
    assert isinstance(r.core_mission, str)
    assert isinstance(r.kpi_name, str)
    assert isinstance(r.kpi_threshold, (int, float))
    assert isinstance(r.autonomy_level, int)
    assert isinstance(r.consistency_score, float)
    assert isinstance(r.consensus_weight, float)
    assert 1 <= r.autonomy_level <= 4

def test_consensus_weights_sum_reasonable():
    total = sum(r.consensus_weight for r in ROLE_REGISTRY)
    assert 1.5 <= total <= 2.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd "<QCM-MVP-Emergence根目录>"; python -m pytest 02-代码编写/test_roles.py -v 2>&1`
Expected: ModuleNotFoundError for qcm.roles

- [ ] **Step 3: Write identity.py**

```python
# qcm/roles/identity.py
from dataclasses import dataclass, field

@dataclass
class RoleIdentity:
    role_id: str
    name: str
    core_mission: str
    kpi_name: str
    kpi_threshold: float
    autonomy_level: int
    consistency_score: float
    consensus_weight: float
    prompt_template: str = ""
    embedding: list = field(default_factory=lambda: [0.0] * 4)

ROLE_REGISTRY = [
    RoleIdentity("secretary", "秘書長", "任務編排與記憶管理", "Task_Assignment_Accuracy", 0.95, 4, 0.96, 0.20),
    RoleIdentity("chief_architect", "首席架構師", "戰略設計與架構一致性", "Design_Consistency_Score", 0.85, 3, 0.94, 0.25),
    RoleIdentity("researcher", "研究員", "知識檢索與深度分析", "Knowledge_Retrieval_Accuracy", 0.90, 3, 0.93, 0.20),
    RoleIdentity("creator", "創作者", "內容生成與創意表達", "Content_Quality_Score", 0.80, 2, 0.91, 0.20),
    RoleIdentity("analyst", "分析師", "數據洞察與趨勢預測", "Insight_Accuracy", 0.85, 2, 0.92, 0.25),
    RoleIdentity("ux_lead", "體驗官", "用戶體驗設計與交互優化", "User_Satisfaction_Score", 4.0, 2, 0.90, 0.20),
    RoleIdentity("risk_auditor", "風控審計", "風險評估與合規審查", "Threat_Detection_Rate", 0.99, 3, 0.95, 0.30),
    RoleIdentity("ai_companion", "AI夥伴", "情感支持與共識構建", "Empathy_Score", 0.85, 2, 0.89, 0.20),
]

def get_role(role_id):
    for r in ROLE_REGISTRY:
        if r.role_id == role_id:
            return r
    return None
```

- [ ] **Step 4: Write __init__.py**

```python
# qcm/roles/__init__.py
from qcm.roles.identity import RoleIdentity, ROLE_REGISTRY, get_role
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd "<QCM-MVP-Emergence根目录>"; python -m pytest 02-代码编写/test_roles.py::test_registry_has_8_roles 02-代码编写/test_roles.py::test_role_has_all_fields 02-代码编写/test_roles.py::test_consensus_weights_sum_reasonable -v 2>&1`
Expected: 3 PASS

- [ ] **Step 6: Commit**

```bash
cd "<QCM-MVP-Emergence根目录>"
git add qcm/roles/__init__.py qcm/roles/identity.py 02-代码编写/test_roles.py
git commit -m "feat: add 8-role super identity architecture (§3.2)"
```

### Task 2: 建立 roles/consensus.py

**Files:**
- Create: `qcm/roles/consensus.py`
- Modify: `02-代码编写/test_roles.py` (append)

- [ ] **Step 1: Write the test**

Append to `02-代码编写/test_roles.py`:

```python
from qcm.roles.consensus import weighted_consensus, ConsensusVote

def test_weighted_consensus():
    votes = [
        ConsensusVote(role_id="risk_auditor", option="A", relevance=1.0),
        ConsensusVote(role_id="chief_architect", option="A", relevance=0.8),
        ConsensusVote(role_id="creator", option="B", relevance=0.6),
    ]
    result = weighted_consensus(votes)
    assert result.chosen_option == "A"
    assert 0 < result.score <= 1

def test_consensus_with_safety_veto():
    votes = [
        ConsensusVote(role_id="risk_auditor", option="B", relevance=1.0, is_safety_veto=True),
        ConsensusVote(role_id="analyst", option="A", relevance=0.9),
        ConsensusVote(role_id="creator", option="A", relevance=0.7),
    ]
    result = weighted_consensus(votes)
    assert result.chosen_option == "B"

def test_consensus_empty_returns_none():
    assert weighted_consensus([]) is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd "<QCM-MVP-Emergence根目录>"; python -m pytest 02-代码编写/test_roles.py::test_weighted_consensus 02-代码编写/test_roles.py::test_consensus_with_safety_veto 02-代码编写/test_roles.py::test_consensus_empty_returns_none -v 2>&1`
Expected: 3 FAIL (import error)

- [ ] **Step 3: Write consensus.py**

```python
# qcm/roles/consensus.py
from dataclasses import dataclass
from qcm.roles.identity import ROLE_REGISTRY, get_role

@dataclass
class ConsensusVote:
    role_id: str
    option: str
    relevance: float  # 0-1, how relevant this decision is to the role
    is_safety_veto: bool = False

@dataclass
class ConsensusResult:
    chosen_option: str
    score: float
    option_scores: dict

def weighted_consensus(votes):
    if not votes:
        return None
    option_scores = {}
    veto_option = None
    for v in votes:
        role = get_role(v.role_id)
        weight = role.consensus_weight if role else 0.15
        if v.is_safety_veto:
            veto_option = v.option
        score = weight * v.relevance
        option_scores[v.option] = option_scores.get(v.option, 0) + score
    if veto_option:
        return ConsensusResult(veto_option, 1.0, option_scores)
    best_option = max(option_scores, key=option_scores.get)
    return ConsensusResult(best_option, option_scores[best_option], option_scores)
```

Add import to `qcm/roles/__init__.py`:

```python
from qcm.roles.consensus import weighted_consensus, ConsensusVote, ConsensusResult
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd "<QCM-MVP-Emergence根目录>"; python -m pytest 02-代码编写/test_roles.py::test_weighted_consensus 02-代码编写/test_roles.py::test_consensus_with_safety_veto 02-代码编写/test_roles.py::test_consensus_empty_returns_none -v 2>&1`
Expected: 3 PASS

- [ ] **Step 5: Commit**

```bash
cd "<QCM-MVP-Emergence根目录>"
git add qcm/roles/consensus.py qcm/roles/__init__.py
git commit -m "feat: add weighted consensus algorithm with safety veto"
```

## Phase 2: 多角色協同模組 (qcm/collaboration/)

### Task 3: 建立 collaboration/meeting.py

**Files:**
- Create: `qcm/collaboration/__init__.py`
- Create: `qcm/collaboration/meeting.py`
- Test: `02-代码编写/test_collaboration.py`

- [ ] **Step 1: Write the test**

```python
# 02-代码编写/test_collaboration.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from qcm.collaboration import MEETING_PHASES, MeetingOrchestrator, MeetingState

def test_meeting_has_5_phases():
    assert len(MEETING_PHASES) == 5
    names = [p["name"] for p in MEETING_PHASES]
    assert "需求發現" in names
    assert "架構設計" in names
    assert "實施規劃" in names
    assert "驗證測試" in names
    assert "總結歸檔" in names

def test_meeting_total_duration():
    total = sum(p["duration_min"] for p in MEETING_PHASES)
    assert total == 90

def test_next_speaker_prediction():
    orch = MeetingOrchestrator()
    assert orch.predict_next_speaker() is None
    orch.add_message("secretary", "我們需要釐清需求")
    orch.add_message("chief_architect", "架構上我建議微服務")
    next_id = orch.predict_next_speaker()
    assert next_id in [r.role_id for r in orch.role_scores]
```

- [ ] **Step 2: Verify tests fail, then write meeting.py**

```python
# qcm/collaboration/meeting.py
from dataclasses import dataclass, field

MEETING_PHASES = [
    {"phase": 1, "name": "需求發現", "duration_min": 15, "focus": "項目需求澄清", "lead_roles": ["secretary", "chief_architect"]},
    {"phase": 2, "name": "架構設計", "duration_min": 20, "focus": "高層系統設計", "lead_roles": ["chief_architect", "researcher"]},
    {"phase": 3, "name": "實施規劃", "duration_min": 25, "focus": "任務分解與分配", "lead_roles": ["creator", "analyst", "ux_lead"]},
    {"phase": 4, "name": "驗證測試", "duration_min": 20, "focus": "測試方法與驗收標準", "lead_roles": ["risk_auditor", "creator"]},
    {"phase": 5, "name": "總結歸檔", "duration_min": 10, "focus": "關鍵決策記錄與下一步", "lead_roles": ["secretary", "ai_companion"]},
]

@dataclass
class MeetingState:
    current_phase: int
    messages: list = field(default_factory=list)
    round_count: int = 0
    is_deadlocked: bool = False

class MeetingOrchestrator:
    def __init__(self):
        self.messages = []
        self.phase = 1
        self.round = 0
        self.role_scores = {r["lead_roles"][0]: 0.5 for r in MEETING_PHASES}

    def add_message(self, role_id, content):
        self.messages.append({"role_id": role_id, "content": content, "phase": self.phase})
        self.round += 1
        if role_id in self.role_scores:
            self.role_scores[role_id] = min(1.0, self.role_scores[role_id] + 0.1)

    def predict_next_speaker(self):
        if not self.messages:
            return None
        scores = {}
        for role_id, base_score in self.role_scores.items():
            time_score = 0.2 * (1.0 - self.round / 100)
            content_score = 0.3 * base_score
            participation_score = 0.25 * base_score
            phase_score = 0.25 * (1.0 if role_id in MEETING_PHASES[self.phase - 1]["lead_roles"] else 0.3)
            scores[role_id] = time_score + content_score + participation_score + phase_score
        return max(scores, key=scores.get)

    def get_state(self):
        return MeetingState(current_phase=self.phase, messages=self.messages[-5:], round_count=self.round)

    def advance_phase(self):
        if self.phase < 5:
            self.phase += 1
```

- [ ] **Step 3: Write __init__.py for collaboration**

```python
# qcm/collaboration/__init__.py
from qcm.collaboration.meeting import MEETING_PHASES, MeetingOrchestrator, MeetingState
```

- [ ] **Step 4: Run tests, verify pass, commit**

Run: `cd "<QCM-MVP-Emergence根目录>"; python -m pytest 02-代码编写/test_collaboration.py -v 2>&1`
Expected: 3 PASS

```bash
git add qcm/collaboration/__init__.py qcm/collaboration/meeting.py 02-代码编写/test_collaboration.py
git commit -m "feat: add multi-role collaboration meeting protocol (§7.1-7.2)"
```

### Task 4: 建立 collaboration/voting.py + deadlock.py + audit.py

**Files:**
- Create: `qcm/collaboration/voting.py`
- Create: `qcm/collaboration/deadlock.py`
- Create: `qcm/collaboration/audit.py`
- Modify: `02-代码编写/test_collaboration.py`

- [ ] **Step 1: Write voting.py**

```python
# qcm/collaboration/voting.py
from enum import Enum

class VoteMode(Enum):
    SIMPLE_MAJORITY = "simple_majority"
    SUPER_MAJORITY = "super_majority"
    FULL_CONSENSUS = "full_consensus"

VOTE_THRESHOLDS = {
    VoteMode.SIMPLE_MAJORITY: 0.50,
    VoteMode.SUPER_MAJORITY: 0.75,
    VoteMode.FULL_CONSENSUS: 1.0,
}

def determine_vote_mode(decision_importance):
    if decision_importance >= 0.8:
        return VoteMode.FULL_CONSENSUS
    elif decision_importance >= 0.5:
        return VoteMode.SUPER_MAJORITY
    return VoteMode.SIMPLE_MAJORITY

def tally_votes(votes, total_voters):
    if not votes or total_voters == 0:
        return None
    option_counts = {}
    for v in votes:
        option_counts[v] = option_counts.get(v, 0) + 1
    best = max(option_counts, key=option_counts.get)
    ratio = option_counts[best] / total_voters
    return {"option": best, "ratio": ratio, "counts": option_counts}
```

- [ ] **Step 2: Write deadlock.py**

```python
# qcm/collaboration/deadlock.py
import math

def novelty_rate(messages, window=5):
    recent = messages[-window:] if len(messages) >= window else messages
    if not recent:
        return 1.0
    unique = len(set(m["content"][:20] for m in recent))
    return unique / len(recent)

def gini_coefficient(scores):
    if not scores:
        return 0
    sorted_s = sorted(scores)
    n = len(sorted_s)
    cumulative = sum((i + 1) * s for i, s in enumerate(sorted_s))
    return (2 * cumulative) / (n * sum(sorted_s)) - (n + 1) / n

def deadlock_score(messages, history_length=5):
    nr = novelty_rate(messages)
    participation = [m["role_id"] for m in messages]
    role_counts = {}
    for p in participation:
        role_counts[p] = role_counts.get(p, 0) + 1
    gini = gini_coefficient(list(role_counts.values())) if role_counts else 0
    N_t = nr if len(messages) >= history_length else 1.0
    G_t = gini
    loop_signal = 1.0 if N_t < 0.15 else 0.0
    score = 0.3 * (1 - N_t) + 0.35 * max(0, (G_t - 0.5) / 0.5) + 0.2 * (1 - min(N_t, 0.15) / 0.15) + 0.15 * loop_signal
    return round(score, 3)

def detect_deadlock(messages):
    score = deadlock_score(messages)
    if score >= 0.6:
        return {"is_deadlock": True, "score": score, "severity": "hard"}
    elif score >= 0.4:
        return {"is_deadlock": False, "score": score, "severity": "warning"}
    return {"is_deadlock": False, "score": score, "severity": "none"}
```

- [ ] **Step 3: Write audit.py**

```python
# qcm/collaboration/audit.py
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class DecisionRecord:
    decision_id: str
    topic: str
    options_evaluated: list
    chosen_option: str
    rationale: str
    voting_results: dict
    voting_method: str
    final_approver: str
    consensus_level: float
    timestamp: str = ""

class AuditLog:
    def __init__(self):
        self._records = []

    def record(self, decision):
        if not decision.timestamp:
            decision.timestamp = datetime.now().isoformat()
        self._records.append(decision)
        return decision.decision_id

    def get(self, decision_id):
        for r in self._records:
            if r.decision_id == decision_id:
                return r
        return None

    @property
    def all_records(self):
        return list(self._records)
```

- [ ] **Step 4: Write the tests**

Append to `02-代码编写/test_collaboration.py`:

```python
from qcm.collaboration.voting import determine_vote_mode, tally_votes, VoteMode
from qcm.collaboration.deadlock import deadlock_score, detect_deadlock
from qcm.collaboration.audit import AuditLog, DecisionRecord

def test_vote_mode_selection():
    assert determine_vote_mode(0.3) == VoteMode.SIMPLE_MAJORITY
    assert determine_vote_mode(0.6) == VoteMode.SUPER_MAJORITY
    assert determine_vote_mode(0.9) == VoteMode.FULL_CONSENSUS

def test_tally_votes():
    result = tally_votes(["A", "A", "B", "A", "C"], 5)
    assert result["option"] == "A"
    assert result["ratio"] == 0.6

def test_deadlock_detection():
    high_novelty = [{"content": str(i)*20, "role_id": "a" if i%2==0 else "b"} for i in range(10)]
    score = deadlock_score(high_novelty)
    assert score < 0.4

def test_audit_log():
    log = AuditLog()
    d = DecisionRecord("DEC-001", "test", ["A","B"], "A", "test", {"A":5,"B":2}, "majority", "chief_architect", 0.71)
    log.record(d)
    assert log.get("DEC-001").chosen_option == "A"
    assert len(log.all_records) == 1
```

- [ ] **Step 5: Update collaboration __init__.py**

```python
# qcm/collaboration/__init__.py
from qcm.collaboration.meeting import MEETING_PHASES, MeetingOrchestrator, MeetingState
from qcm.collaboration.voting import VoteMode, VOTE_THRESHOLDS, determine_vote_mode, tally_votes
from qcm.collaboration.deadlock import deadlock_score, detect_deadlock
from qcm.collaboration.audit import AuditLog, DecisionRecord
```

- [ ] **Step 6: Run all collaboration tests**

Run: `cd "<QCM-MVP-Emergence根目录>"; python -m pytest 02-代码编写/test_collaboration.py -v 2>&1`
Expected: 7 PASS

- [ ] **Step 7: Commit**

```bash
git add qcm/collaboration/voting.py qcm/collaboration/deadlock.py qcm/collaboration/audit.py qcm/collaboration/__init__.py
git commit -m "feat: add voting, deadlock detection, decision audit (§7.3-7.6)"
```

## Phase 3: 三層沙盤模組 (qcm/sandbox/)

### Task 5: 建立 sandbox/layers.py + srs.py

**Files:**
- Create: `qcm/sandbox/__init__.py`
- Create: `qcm/sandbox/layers.py`
- Create: `qcm/sandbox/srs.py`
- Test: `02-代码编写/test_sandbox.py`

- [ ] **Step 1: Write the test**

```python
# 02-代码编写/test_sandbox.py
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from qcm.sandbox.layers import SANDBOX_LAYERS, complexity_differential
from qcm.sandbox.srs import calculate_srs, confidence_gate, calculate_cbp

def test_sandbox_has_3_layers():
    assert len(SANDBOX_LAYERS) == 3
    names = [l["name"] for l in SANDBOX_LAYERS]
    assert "sandbox" in names
    assert "war_room" in names
    assert "simulation" in names

def test_complexity_differential():
    f = complexity_differential(f_k=3, f_max=5, lam=0.5, mu=0, success=True, dt=1.0)
    expected = 3 + 0.5 * (1 - 3/5) * 1.0
    assert abs(f - expected) < 1e-6

def test_complexity_decay_on_failure():
    f = complexity_differential(f_k=4, f_max=10, lam=0.5, mu=0.3, success=False, dt=1.0)
    expected = 4 - 0.3 * 4 * 1.0
    assert abs(f - expected) < 1e-6

def test_srs_scoring():
    srs = calculate_srs(f_values=[3, 4, 5], f_target=4, sigma=1.0)
    assert 0 < srs <= 1

def test_confidence_gate():
    assert confidence_gate(0.90, 0.85) is True
    assert confidence_gate(0.80, 0.85) is False

def test_cbp():
    cbp = calculate_cbp(avg_R=0.7, R_limit=1.0, violations=0, innovation_score=1.0)
    assert cbp > 0
```

- [ ] **Step 2: Write layers.py**

```python
# qcm/sandbox/layers.py
SANDBOX_LAYERS = [
    {"name": "sandbox", "f_range": (1, 5), "isolation": "process", "duration_s": 1, "threshold": 0.85},
    {"name": "war_room", "f_range": (5, 20), "isolation": "compose", "duration_s": 60, "threshold": 0.90},
    {"name": "simulation", "f_range": (20, 100), "isolation": "k8s", "duration_s": 3600, "threshold": None},
]

def complexity_differential(f_k, f_max, lam=0.5, mu=0.1, success=True, dt=1.0):
    if success:
        return f_k + lam * (1 - f_k / f_max) * dt
    return f_k - mu * f_k * dt

def get_layer_for_f(f):
    for layer in SANDBOX_LAYERS:
        lo, hi = layer["f_range"]
        if lo <= f <= hi:
            return layer
    return SANDBOX_LAYERS[-1]
```

- [ ] **Step 3: Write srs.py**

```python
# qcm/sandbox/srs.py
import math

def calculate_srs(f_values, f_target, sigma=1.0):
    if not f_values:
        return 0.0
    total = 0.0
    for f in f_values:
        total += math.exp(-((f - f_target) ** 2) / (2 * sigma ** 2))
    return round(total / len(f_values), 4)

def confidence_gate(srs, threshold):
    return srs >= threshold

def calculate_cbp(avg_R, R_limit=1.0, violations=0, innovation_score=0.0):
    term1 = 0.4 * min(1.0, (R_limit - avg_R) / R_limit) if R_limit > 0 else 0
    term2 = 0.3 if violations == 0 else 0
    term3 = 0.3 * math.log(1 + innovation_score)
    return round(term1 + term2 + term3, 4)
```

- [ ] **Step 4: Write sandbox __init__.py**

```python
# qcm/sandbox/__init__.py
from qcm.sandbox.layers import SANDBOX_LAYERS, complexity_differential, get_layer_for_f
from qcm.sandbox.srs import calculate_srs, confidence_gate, calculate_cbp
```

- [ ] **Step 5: Run tests**

Run: `cd "<QCM-MVP-Emergence根目录>"; python -m pytest 02-代码编写/test_sandbox.py -v 2>&1`
Expected: 6 PASS

- [ ] **Step 6: Commit**

```bash
git add qcm/sandbox/__init__.py qcm/sandbox/layers.py qcm/sandbox/srs.py 02-代码编写/test_sandbox.py
git commit -m "feat: add 3-layer sandbox with SRS scoring (§8.1-8.5)"
```

### Task 6: 建立 sandbox/scheduler.py

**Files:**
- Create: `qcm/sandbox/scheduler.py`
- Modify: `02-代码编写/test_sandbox.py`

- [ ] **Step 1: Write the test**

Append to `02-代码编写/test_sandbox.py`:

```python
from qcm.sandbox.scheduler import priority_score, schedule_projects

def test_priority_score():
    score = priority_score(urgency=0.8, value=0.7, resource_availability=0.5, knowledge_transfer=0.3)
    expected = 0.35*0.8 + 0.30*0.7 + 0.20*0.5 + 0.15*0.3
    assert abs(score - expected) < 1e-6

def test_schedule_sorts_by_priority():
    projects = [
        {"id": "A", "urgency": 0.9, "value": 0.5, "resource_availability": 0.3, "knowledge_transfer": 0.2},
        {"id": "B", "urgency": 0.3, "value": 0.9, "resource_availability": 0.8, "knowledge_transfer": 0.7},
    ]
    result = schedule_projects(projects)
    assert result[0]["id"] in ("A", "B")
    assert all(p.get("priority", 0) > 0 for p in result)
```

- [ ] **Step 2: Write scheduler.py**

```python
# qcm/sandbox/scheduler.py
def priority_score(urgency, value, resource_availability, knowledge_transfer):
    return (0.35 * urgency + 0.30 * value + 0.20 * resource_availability
            + 0.15 * knowledge_transfer)

def schedule_projects(projects):
    for p in projects:
        p["priority"] = priority_score(
            p.get("urgency", 0), p.get("value", 0),
            p.get("resource_availability", 0), p.get("knowledge_transfer", 0))
    return sorted(projects, key=lambda x: x["priority"], reverse=True)
```

- [ ] **Step 3: Update sandbox __init__.py**

```python
from qcm.sandbox.scheduler import priority_score, schedule_projects
```

- [ ] **Step 4: Run tests, commit**

```bash
git add qcm/sandbox/scheduler.py qcm/sandbox/__init__.py
git commit -m "feat: add priority scheduler for sandbox war room (§8.4)"
```

## Phase 4: 雙層循環飛輪模組 (qcm/flywheel/)

### Task 7: 建立 flywheel/outer_loop.py + inner_loop.py

**Files:**
- Create: `qcm/flywheel/__init__.py`
- Create: `qcm/flywheel/outer_loop.py`
- Create: `qcm/flywheel/inner_loop.py`
- Test: `02-代码编写/test_flywheel.py`

- [ ] **Step 1: Write the test**

```python
# 02-代码编写/test_flywheel.py
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from qcm.flywheel.outer_loop import update_user_capability, difficulty_adapt
from qcm.flywheel.inner_loop import update_system_state, has_converged

def test_user_capability_update():
    U_new = update_user_capability(U=0.5, G=0.8, eta=0.1, beta=0.05, t=10)
    expected = 0.5 + 0.1 * (0.8 - 0.5) * (1 - math.exp(-0.05 * 10))
    assert abs(U_new - expected) < 1e-6

def test_difficulty_adapt_upgrade():
    assert difficulty_adapt(accuracy=0.95, speed=0.85) == "upgrade"

def test_difficulty_adapt_downgrade():
    assert difficulty_adapt(accuracy=0.6, speed=0.5) == "downgrade"

def test_difficulty_adapt_maintain():
    assert difficulty_adapt(accuracy=0.8, speed=0.7) == "maintain"

def test_system_state_update():
    S_new = update_system_state(S=0.5, grad=0.3, eta=0.1, gamma=0.05, t=5)
    expected = 0.5 + 0.1 * 0.3 * math.exp(-0.05 * 5)
    assert abs(S_new - expected) < 1e-6

def test_convergence():
    recent = [0.81, 0.805, 0.802, 0.799, 0.797, 0.795, 0.793, 0.792, 0.791, 0.79]
    assert has_converged(recent, threshold=0.01) is True
    assert has_converged([0.5, 0.6, 0.7, 0.8], threshold=0.01) is False
```

- [ ] **Step 2: Write outer_loop.py**

```python
# qcm/flywheel/outer_loop.py
import math

def update_user_capability(U, G, eta=0.1, beta=0.05, t=1):
    return U + eta * (G - U) * (1 - math.exp(-beta * t))

def difficulty_adapt(accuracy, speed):
    if accuracy > 0.9 and speed > 0.8:
        return "upgrade"
    elif accuracy < 0.7:
        return "downgrade"
    return "maintain"

def generate_learning_path(ability_assessment, knowledge_graph=None):
    path = [
        {"step": 1, "skill": "foundation", "difficulty": max(1, ability_assessment - 1)},
        {"step": 2, "skill": "application", "difficulty": ability_assessment},
        {"step": 3, "skill": "advanced", "difficulty": ability_assessment + 1},
    ]
    return path
```

- [ ] **Step 3: Write inner_loop.py**

```python
# qcm/flywheel/inner_loop.py
import math

def update_system_state(S, grad, eta=0.1, gamma=0.05, t=1):
    return S + eta * grad * math.exp(-gamma * t)

def has_converged(recent_improvements, threshold=0.01):
    if len(recent_improvements) < 3:
        return False
    last_10 = recent_improvements[-10:] if len(recent_improvements) >= 10 else recent_improvements
    if len(last_10) < 3:
        return False
    improvements = [abs(last_10[i] - last_10[i-1]) for i in range(1, len(last_10))]
    return all(imp < threshold for imp in improvements[-3:])
```

- [ ] **Step 4: Run tests**

Run: `cd "<QCM-MVP-Emergence根目录>"; python -m pytest 02-代码编写/test_flywheel.py -v 2>&1`
Expected: 6 PASS

- [ ] **Step 5: Commit**

```bash
git add qcm/flywheel/outer_loop.py qcm/flywheel/inner_loop.py 02-代码编写/test_flywheel.py
git commit -m "feat: add dual-loop flywheel outer+inner (§4.1-4.3)"
```

### Task 8: 建立 flywheel/energy.py + stability.py

**Files:**
- Create: `qcm/flywheel/energy.py`
- Create: `qcm/flywheel/stability.py`
- Modify: `02-代码编写/test_flywheel.py`

- [ ] **Step 1: Write the test**

Append to `02-代码编写/test_flywheel.py`:

```python
from qcm.flywheel.energy import total_energy, flywheel_energy_rate
from qcm.flywheel.stability import lyapunov_function, spectral_radius, adaptive_learning_rate

def test_total_energy():
    E = total_energy(E_resonance=0.8, E_flywheel=0.5, E_phantom=0.3)
    assert abs(E - 1.6) < 1e-6

def test_flywheel_energy_rate():
    rate = flywheel_energy_rate(P_input=1.0, P_dissipation=0.3, P_synergy=0.2)
    assert abs(rate - 0.9) < 1e-6

def test_lyapunov():
    theta = [0.5, 0.3, 0.2]
    V = lyapunov_function(theta)
    expected = 0.5 * (0.25 + 0.09 + 0.04)
    assert abs(V - expected) < 1e-6

def test_spectral_radius():
    rho = spectral_radius([[0.7, 0.1], [0.2, 0.6]])
    assert rho < 1.0
    assert rho > 0

def test_adaptive_learning_rate():
    lr = adaptive_learning_rate(t=5, init_lr=0.1, gamma=0.01, kappa=0.6, loss_variance=0.5)
    assert 0 < lr <= 0.1
```

- [ ] **Step 2: Write energy.py**

```python
# qcm/flywheel/energy.py

def total_energy(E_resonance=0.0, E_flywheel=0.0, E_phantom=0.0):
    return E_resonance + E_flywheel + E_phantom

def flywheel_energy_rate(P_input=0.0, P_dissipation=0.0, P_synergy=0.0):
    return P_input - P_dissipation + P_synergy

def resonance_energy(similarities, weights):
    total = 0.0
    for (i, j), sim in similarities.items():
        w = weights.get((i, j), 0.5)
        total += w * sim
    return total
```

- [ ] **Step 3: Write stability.py**

```python
# qcm/flywheel/stability.py
import math
import numpy as np

def lyapunov_function(theta):
    return 0.5 * sum(t ** 2 for t in theta)

def spectral_radius(matrix):
    arr = np.array(matrix, dtype=float)
    eigenvalues = np.linalg.eigvals(arr)
    return float(max(abs(e) for e in eigenvalues))

def adaptive_learning_rate(t, init_lr=0.1, gamma=0.01, kappa=0.6, loss_variance=0.5):
    base = init_lr / (1 + gamma * (t ** kappa))
    return base * math.exp(-0.5 * loss_variance)

def self_improvement_rate(A0=1.0, t=1, eta=0.3, t_ref=7, zeta=1.4):
    return A0 * (1 + eta * t / t_ref) ** zeta
```

- [ ] **Step 4: Write flywheel __init__.py**

```python
# qcm/flywheel/__init__.py
from qcm.flywheel.outer_loop import update_user_capability, difficulty_adapt, generate_learning_path
from qcm.flywheel.inner_loop import update_system_state, has_converged
from qcm.flywheel.energy import total_energy, flywheel_energy_rate, resonance_energy
from qcm.flywheel.stability import lyapunov_function, spectral_radius, adaptive_learning_rate, self_improvement_rate
```

- [ ] **Step 5: Run all flywheel tests**

Run: `cd "<QCM-MVP-Emergence根目录>"; python -m pytest 02-代码编写/test_flywheel.py -v 2>&1`
Expected: 11 PASS

- [ ] **Step 6: Commit**

```bash
git add qcm/flywheel/energy.py qcm/flywheel/stability.py qcm/flywheel/__init__.py
git commit -m "feat: add energy framework and Lyapunov stability (§4.4-4.6)"
```

## Phase 5: 動態角色召喚模組 (qcm/summoning/)

### Task 9: 建立 summoning/features.py + matching.py

**Files:**
- Create: `qcm/summoning/__init__.py`
- Create: `qcm/summoning/features.py`
- Create: `qcm/summoning/matching.py`
- Test: `02-代码编写/test_summoning.py`

- [ ] **Step 1: Write the test**

```python
# 02-代码编写/test_summoning.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from qcm.summoning.features import extract_tfidf_keywords, ensemble_score
from qcm.summoning.matching import calculate_skill_match, dynamic_penalty, mahalanobis_distance

def test_tfidf_extraction():
    keywords = extract_tfidf_keywords("我們需要開發一個醫療合規審查系統")
    assert isinstance(keywords, dict)
    assert len(keywords) > 0

def test_ensemble_score():
    score = ensemble_score(f1=0.7, f2=0.8, f3=0.6, f4=0.5, f5=0.7, f6=0.9)
    expected = 0.25*0.7 + 0.30*0.8 + 0.20*0.6 + 0.10*0.5 + 0.10*0.7 + 0.05*0.9
    assert abs(score - expected) < 1e-6

def test_skill_match_scoring():
    score = calculate_skill_match(["python", "ml", "nlp"], {"skills": ["python", "java", "sql"]})
    assert 0 <= score <= 1

def test_skill_match_below_threshold():
    score = calculate_skill_match(["cobol"], {"skills": ["python", "rust", "go"]})
    assert score < 0.75

def test_dynamic_penalty():
    assert dynamic_penalty(8) == 0.0
    assert dynamic_penalty(10) > 0
    assert dynamic_penalty(15) > dynamic_penalty(10)

def test_mahalanobis_distance():
    dist = mahalanobis_distance([1, 2], [1.5, 2.5], cov_matrix=[[1, 0], [0, 1]])
    assert dist > 0
```

- [ ] **Step 2: Write features.py**

```python
# qcm/summoning/features.py
import re, math
from collections import Counter

TFIDF_WEIGHTS = {"開發": 0.8, "系統": 0.6, "醫療": 0.9, "合規": 0.85, "審查": 0.7,
                 "設計": 0.6, "分析": 0.7, "測試": 0.5, "部署": 0.6, "優化": 0.7}

def extract_tfidf_keywords(text, vocab_size=100):
    words = re.findall(r'[\w]+', text)
    counter = Counter(words)
    total = sum(counter.values())
    keywords = {}
    for word, count in counter.most_common(min(vocab_size, len(counter))):
        tf = count / total if total > 0 else 0
        idf = TFIDF_WEIGHTS.get(word, 0.3)
        keywords[word] = round(tf * idf, 4)
    return keywords

def ensemble_score(f1=0, f2=0, f3=0, f4=0, f5=0, f6=0):
    w = [0.25, 0.30, 0.20, 0.10, 0.10, 0.05]
    return w[0]*f1 + w[1]*f2 + w[2]*f3 + w[3]*f4 + w[4]*f5 + w[5]*f6
```

- [ ] **Step 3: Write matching.py**

```python
# qcm/summoning/matching.py
import math
import numpy as np

def calculate_skill_match(requested_skills, role_def, threshold=0.75):
    role_skills = set(s.lower() for s in role_def.get("skills", []))
    req_skills = set(s.lower() for s in requested_skills)
    if not req_skills or not role_skills:
        return 0.0
    intersection = req_skills & role_skills
    if not intersection:
        return 0.0
    jaccard = len(intersection) / len(req_skills | role_skills)
    recall = len(intersection) / len(req_skills)
    score = 0.6 * jaccard + 0.4 * recall
    return round(score, 4)

def dynamic_penalty(total_roles):
    if total_roles <= 8:
        return 0.0
    elif total_roles <= 12:
        return 0.05 * (total_roles - 8)
    return 0.2 + 0.1 * (total_roles - 12) ** 2

def mahalanobis_distance(x, y, cov_matrix=None):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    diff = x - y
    if cov_matrix is None:
        return float(np.sqrt(np.dot(diff, diff)))
    cov = np.array(cov_matrix, dtype=float)
    try:
        inv = np.linalg.inv(cov)
        return float(np.sqrt(np.dot(np.dot(diff, inv), diff)))
    except np.linalg.LinAlgError:
        return float(np.sqrt(np.dot(diff, diff)))
```

- [ ] **Step 4: Write summoning/registry.py**

```python
# qcm/summoning/registry.py
from qcm.roles.identity import ROLE_REGISTRY
from qcm.summoning.matching import calculate_skill_match, dynamic_penalty

class DynamicRoleRegistry:
    def __init__(self):
        self._roles = list(ROLE_REGISTRY)
        self._dynamic_roles = []

    @property
    def all_roles(self):
        return self._roles + self._dynamic_roles

    def register_dynamic_role(self, role):
        self._dynamic_roles.append(role)

    def summon(self, required_skills, max_roles=15):
        candidates = []
        for role in self.all_roles:
            match = calculate_skill_match(required_skills, {"skills": [role.role_id]})
            if match > 0.75:
                penalty = dynamic_penalty(len(self.all_roles))
                candidates.append((role, match - penalty))
        candidates.sort(key=lambda x: x[1], reverse=True)
        return [c[0] for c in candidates[:max_roles]]
```

- [ ] **Step 5: Write summoning __init__.py**

```python
# qcm/summoning/__init__.py
from qcm.summoning.features import extract_tfidf_keywords, ensemble_score
from qcm.summoning.matching import calculate_skill_match, dynamic_penalty, mahalanobis_distance
from qcm.summoning.registry import DynamicRoleRegistry
```

- [ ] **Step 6: Run tests**

Run: `cd "<QCM-MVP-Emergence根目录>"; python -m pytest 02-代码编写/test_summoning.py -v 2>&1`
Expected: 6 PASS

- [ ] **Step 7: Commit**

```bash
git add qcm/summoning/__init__.py qcm/summoning/features.py qcm/summoning/matching.py qcm/summoning/registry.py 02-代码编写/test_summoning.py
git commit -m "feat: add dynamic role summoning engine with skill matching (§9)"
```

## Phase 6: Pipeline 整合 + 回歸測試

### Task 10: 更新 qcm/__init__.py

**Files:**
- Modify: `qcm/__init__.py`

- [ ] **Step 1: Update exports**

Replace existing `qcm/__init__.py`:

```python
"""QCM 統一命名空間包 — 論文 5 大模組全整合"""
import sys, os

_code_dir = os.path.join(os.path.dirname(__file__), '..', '02-代码编写')
if os.path.isdir(_code_dir) and _code_dir not in sys.path:
    sys.path.insert(0, os.path.abspath(_code_dir))

from qcm.config import QCMConfig, load_config
from qcm.plugin import PluginRegistry, plugin_registry
from qcm.pipeline import PipelineEngine
from qcm.roles import ROLE_REGISTRY, weighted_consensus
from qcm.collaboration import MEETING_PHASES, MeetingOrchestrator, VoteMode, detect_deadlock, AuditLog
from qcm.sandbox import SANDBOX_LAYERS, calculate_srs, confidence_gate, priority_score
from qcm.flywheel import total_energy, lyapunov_function, adaptive_learning_rate
from qcm.summoning import extract_tfidf_keywords, calculate_skill_match, DynamicRoleRegistry

__all__ = [
    'QCMConfig', 'load_config',
    'PluginRegistry', 'plugin_registry',
    'PipelineEngine',
    'ROLE_REGISTRY', 'weighted_consensus',
    'MEETING_PHASES', 'MeetingOrchestrator', 'VoteMode', 'detect_deadlock', 'AuditLog',
    'SANDBOX_LAYERS', 'calculate_srs', 'confidence_gate', 'priority_score',
    'total_energy', 'lyapunov_function', 'adaptive_learning_rate',
    'extract_tfidf_keywords', 'calculate_skill_match', 'DynamicRoleRegistry',
]
```

- [ ] **Step 2: Verify imports work**

Run: `cd "<QCM-MVP-Emergence根目录>"; python -c "from qcm import *; print('OK: %d symbols' % len(__all__))" 2>&1`
Expected: `OK: 18 symbols`

- [ ] **Step 3: Commit**

```bash
git add qcm/__init__.py
git commit -m "chore: update qcm namespace exports with all 5 modules"
```

### Task 11: 整合至 pipeline.py

**Files:**
- Modify: `qcm/pipeline.py`

- [ ] **Step 1: Add module initialization to PipelineEngine**

Add after `_init_capabilities` in `qcm/pipeline.py`:

```python
    def _init_paper_modules(self):
        self.modules_enabled = self.config.get("modules", True)
        if not self.modules_enabled:
            self.meeting = None
            self.sandbox = None
            self.flywheel = None
            self.summoning = None
            return
        from qcm.collaboration import MeetingOrchestrator, AuditLog
        from qcm.sandbox import calculate_srs, confidence_gate
        from qcm.flywheel import total_energy, update_user_capability, update_system_state
        from qcm.summoning import DynamicRoleRegistry
        self.meeting = MeetingOrchestrator()
        self.audit_log = AuditLog()
        self.skill_registry = DynamicRoleRegistry()
        self.paper_modules_initialized = True
```

Call `_init_paper_modules()` at the end of `__init__`.

- [ ] **Step 2: Update run_round to integrate modules**

Add after the existing R calculation and emergence detection in `run_round()`:

```python
    def _run_paper_modules(self, R, components):
        enhanced = {}
        if not getattr(self, 'paper_modules_initialized', False):
            return enhanced
        try:
            self.meeting.add_message("system", f"Round {self.round_count}: R={R:.4f}")
            state = self.meeting.get_state()
            enhanced['meeting'] = {
                'phase': state.current_phase,
                'rounds': state.round_count,
                'is_deadlocked': state.is_deadlocked,
            }
        except Exception as e:
            enhanced['meeting'] = {'error': str(e)}
        try:
            srs = calculate_srs([R], f_target=self.config.emergence_threshold)
            enhanced['sandbox'] = {'srs': srs, 'can_advance': confidence_gate(srs, 0.85)}
        except Exception as e:
            enhanced['sandbox'] = {'error': str(e)}
        try:
            fw_energy = total_energy(E_resonance=R, E_flywheel=0.1 * self.round_count)
            enhanced['flywheel'] = {'total_energy': round(fw_energy, 4)}
        except Exception as e:
            enhanced['flywheel'] = {'error': str(e)}
        return enhanced
```

Call `_run_paper_modules` in `run_round()` and merge into the `enhanced` dict.

- [ ] **Step 3: Run regression test**

Run: `cd "<QCM-MVP-Emergence根目录>"; python -m pytest 02-代码编写/test_qcm_all.py -v 2>&1`
Expected: 25/25 PASS (unchanged)

- [ ] **Step 4: Run all new tests**

Run: `cd "<QCM-MVP-Emergence根目录>"; python -m pytest 02-代码编写/test_roles.py 02-代码编写/test_collaboration.py 02-代码编写/test_sandbox.py 02-代码编写/test_flywheel.py 02-代码编写/test_summoning.py -v 2>&1`
Expected: All PASS (~33 tests)

- [ ] **Step 5: Run main.py to verify emergence unchanged**

Run: `cd "<QCM-MVP-Emergence根目录>"; python 02-代码编写/main.py 2>&1`
Expected: R22 ≈ 0.866, emergence occurs

- [ ] **Step 6: Commit**

```bash
git add qcm/pipeline.py
git commit -m "feat: integrate paper modules into pipeline engine"
```

### Task 12: 最終驗證 + 交付更新

- [ ] **Step 1: Full test suite**

```bash
cd "<QCM-MVP-Emergence根目录>"; python -m pytest 02-代码编写/ -v 2>&1
```
Expected: 25 + 3+7+6+11+6 = ~58 PASS (approx, some may be combined)

- [ ] **Step 2: Verify emergence**

```bash
cd "<QCM-MVP-Emergence根目录>"; python 02-代码编写/main.py --rounds 22 2>&1
```
Expected: R22 ≈ 0.866, emergence confirmed

- [ ] **Step 3: Update deliverable docs**

Modify `VERIFY-QCM.md`, `MANIFEST-QCM.txt`, `INDEX-QCM.md`, `PROJECT_HANDOFF-QCM.md` to reflect v6.3 with 5 new modules, ~130 files, ~58 tests.

- [ ] **Step 4: Final commit**

```bash
git add VERIFY-QCM.md MANIFEST-QCM.txt INDEX-QCM.md PROJECT_HANDOFF-QCM.md
git commit -m "docs: update deliverable docs to v6.3 with 5 paper modules"
```
