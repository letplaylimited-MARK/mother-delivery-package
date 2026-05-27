import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from qcm.sandbox.layers import SANDBOX_LAYERS, complexity_differential
from qcm.sandbox.srs import calculate_srs, confidence_gate, calculate_cbp
from qcm.sandbox.scheduler import priority_score, schedule_projects


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
    assert len(result) == 2
    assert all(p.get("priority", 0) > 0 for p in result)
