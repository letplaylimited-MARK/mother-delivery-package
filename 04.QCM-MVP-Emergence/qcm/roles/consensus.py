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
