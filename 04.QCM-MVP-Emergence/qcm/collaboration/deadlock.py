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
