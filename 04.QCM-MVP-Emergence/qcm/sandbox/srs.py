import math

def calculate_srs(f_values, f_target, sigma=1.0):
    if not f_values:
        return 0.0
    total = 0.0
    for f in f_values:
        total += math.exp(-((f - f_target) ** 2) / (2 * sigma ** 2))
    return round(total / len(f_values), 4)

def confidence_gate(srs, threshold):
    return srs >= threshold

def calculate_cbp(avg_R, R_limit=1.0, violations=0, innovation_score=0.0):
    term1 = 0.4 * min(1.0, (R_limit - avg_R) / R_limit) if R_limit > 0 else 0
    term2 = 0.3 if violations == 0 else 0
    term3 = 0.3 * math.log(1 + innovation_score)
    return round(term1 + term2 + term3, 4)
