def total_energy(E_resonance=0.0, E_flywheel=0.0, E_phantom=0.0):
    return E_resonance + E_flywheel + E_phantom

def flywheel_energy_rate(P_input=0.0, P_dissipation=0.0, P_synergy=0.0):
    return P_input - P_dissipation + P_synergy

def resonance_energy(similarities, weights):
    total = 0.0
    for (i, j), sim in similarities.items():
        w = weights.get((i, j), 0.5)
        total += w * sim
    return total
