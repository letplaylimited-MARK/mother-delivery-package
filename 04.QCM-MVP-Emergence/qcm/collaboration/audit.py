from dataclasses import dataclass
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
