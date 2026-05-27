import numpy as np

def calculate_skill_match(requested_skills, role_def):
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
