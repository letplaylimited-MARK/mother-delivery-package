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
