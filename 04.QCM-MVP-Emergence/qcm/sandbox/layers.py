SANDBOX_LAYERS = [
    {"name": "sandbox", "f_range": (1, 5), "isolation": "process", "duration_s": 1, "threshold": 0.85},
    {"name": "war_room", "f_range": (5, 20), "isolation": "compose", "duration_s": 60, "threshold": 0.90},
    {"name": "simulation", "f_range": (20, 100), "isolation": "k8s", "duration_s": 3600, "threshold": None},
]

def complexity_differential(f_k, f_max, lam=0.5, mu=0.1, success=True, dt=1.0):
    if success:
        return f_k + lam * (1 - f_k / f_max) * dt
    return f_k - mu * f_k * dt

def get_layer_for_f(f):
    for layer in SANDBOX_LAYERS:
        lo, hi = layer["f_range"]
        if lo <= f <= hi:
            return layer
    return SANDBOX_LAYERS[-1]
