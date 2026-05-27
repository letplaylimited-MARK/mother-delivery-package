import math
import numpy as np

def lyapunov_function(theta):
    return 0.5 * sum(t ** 2 for t in theta)

def spectral_radius(matrix):
    arr = np.array(matrix, dtype=float)
    eigenvalues = np.linalg.eigvals(arr)
    return float(max(abs(e) for e in eigenvalues))

def adaptive_learning_rate(t, init_lr=0.1, gamma=0.01, kappa=0.6, loss_variance=0.5):
    base = init_lr / (1 + gamma * (t ** kappa))
    return base * math.exp(-0.5 * loss_variance)

def self_improvement_rate(A0=1.0, t=1, eta=0.3, t_ref=7, zeta=1.4):
    return A0 * (1 + eta * t / t_ref) ** zeta
