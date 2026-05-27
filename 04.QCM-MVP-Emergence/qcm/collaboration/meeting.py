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
