import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from qcm.collaboration import MEETING_PHASES, MeetingOrchestrator, MeetingState
from qcm.collaboration.voting import determine_vote_mode, tally_votes, VoteMode
from qcm.collaboration.deadlock import deadlock_score, detect_deadlock
from qcm.collaboration.audit import AuditLog, DecisionRecord

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
    assert next_id in [r["lead_roles"][0] for r in MEETING_PHASES]

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
