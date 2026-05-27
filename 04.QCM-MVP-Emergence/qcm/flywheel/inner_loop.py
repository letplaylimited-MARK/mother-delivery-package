import math

def update_system_state(S, grad, eta=0.1, gamma=0.05, t=1):
    return S + eta * grad * math.exp(-gamma * t)

def has_converged(recent_improvements, threshold=0.01):
    if len(recent_improvements) < 3:
        return False
    last_10 = recent_improvements[-10:] if len(recent_improvements) >= 10 else recent_improvements
    if len(last_10) < 3:
        return False
    improvements = [abs(last_10[i] - last_10[i-1]) for i in range(1, len(last_10))]
    return all(imp < threshold for imp in improvements[-3:])
