import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from qcm.flywheel.outer_loop import update_user_capability, difficulty_adapt
from qcm.flywheel.inner_loop import update_system_state, has_converged
from qcm.flywheel.energy import total_energy, flywheel_energy_rate
from qcm.flywheel.stability import lyapunov_function, spectral_radius, adaptive_learning_rate


def test_user_capability_update():
    U_new = update_user_capability(U=0.5, G=0.8, eta=0.1, beta=0.05, t=10)
    expected = 0.5 + 0.1 * (0.8 - 0.5) * (1 - math.exp(-0.05 * 10))
    assert abs(U_new - expected) < 1e-6

def test_difficulty_adapt_upgrade():
    assert difficulty_adapt(accuracy=0.95, speed=0.85) == "upgrade"

def test_difficulty_adapt_downgrade():
    assert difficulty_adapt(accuracy=0.6, speed=0.5) == "downgrade"

def test_difficulty_adapt_maintain():
    assert difficulty_adapt(accuracy=0.8, speed=0.7) == "maintain"

def test_system_state_update():
    S_new = update_system_state(S=0.5, grad=0.3, eta=0.1, gamma=0.05, t=5)
    expected = 0.5 + 0.1 * 0.3 * math.exp(-0.05 * 5)
    assert abs(S_new - expected) < 1e-6

def test_convergence():
    recent = [0.81, 0.805, 0.802, 0.799, 0.797, 0.795, 0.793, 0.792, 0.791, 0.79]
    assert has_converged(recent, threshold=0.01) is True
    assert has_converged([0.5, 0.6, 0.7, 0.8], threshold=0.01) is False

def test_total_energy():
    E = total_energy(E_resonance=0.8, E_flywheel=0.5, E_phantom=0.3)
    assert abs(E - 1.6) < 1e-6

def test_flywheel_energy_rate():
    rate = flywheel_energy_rate(P_input=1.0, P_dissipation=0.3, P_synergy=0.2)
    assert abs(rate - 0.9) < 1e-6

def test_lyapunov():
    theta = [0.5, 0.3, 0.2]
    V = lyapunov_function(theta)
    expected = 0.5 * (0.25 + 0.09 + 0.04)
    assert abs(V - expected) < 1e-6

def test_spectral_radius():
    rho = spectral_radius([[0.7, 0.1], [0.2, 0.6]])
    assert rho < 1.0
    assert rho > 0

def test_adaptive_learning_rate():
    lr = adaptive_learning_rate(t=5, init_lr=0.1, gamma=0.01, kappa=0.6, loss_variance=0.5)
    assert 0 < lr <= 0.1
