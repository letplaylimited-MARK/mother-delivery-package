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
    RoleIdentity("ux_lead", "體驗官", "用戶體驗設計與交互優化", "User_Satisfaction_Score", 0.80, 2, 0.90, 0.20),
    RoleIdentity("risk_auditor", "風控審計", "風險評估與合規審查", "Threat_Detection_Rate", 0.99, 3, 0.95, 0.30),
    RoleIdentity("ai_companion", "AI夥伴", "情感支持與共識構建", "Empathy_Score", 0.85, 2, 0.89, 0.20),
]

def get_role(role_id):
    for r in ROLE_REGISTRY:
        if r.role_id == role_id:
            return r
    return None
