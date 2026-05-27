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
