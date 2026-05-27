import math

def update_user_capability(U, G, eta=0.1, beta=0.05, t=1):
    return U + eta * (G - U) * (1 - math.exp(-beta * t))

def difficulty_adapt(accuracy, speed):
    if accuracy > 0.9 and speed > 0.8:
        return "upgrade"
    elif accuracy < 0.7:
        return "downgrade"
    return "maintain"

def generate_learning_path(ability_assessment, knowledge_graph=None):
    path = [
        {"step": 1, "skill": "foundation", "difficulty": max(1, ability_assessment - 1)},
        {"step": 2, "skill": "application", "difficulty": ability_assessment},
        {"step": 3, "skill": "advanced", "difficulty": ability_assessment + 1},
    ]
    return path
