"""Config sync assertion test — verifies calculator.py and detector.py constants match qcm/config.py.

If someone modifies DEFAULT_CONFIG in qcm/config.py without updating the class constants
in calculator.py or detector.py, this test will FAIL — providing an early warning.

Note: These class constants exist due to circular dependency (calculator.py cannot lazy-import
config.py). This test serves as the synchronization guard rail.
"""

import sys
import os

# Ensure qcm package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcm.config import DEFAULT_CONFIG
from calculator import ResonanceCalculator
from detector import EmergenceDetector


def test_calculator_weights_match_config():
    """Verify ResonanceCalculator class constants match DEFAULT_CONFIG.paper_params.calculator"""
    cfg = DEFAULT_CONFIG["paper_params"]["calculator"]
    assert ResonanceCalculator.W_K == cfg["W_K"], f"W_K mismatch: class={ResonanceCalculator.W_K}, config={cfg['W_K']}"
    assert ResonanceCalculator.W_C == cfg["W_C"], f"W_C mismatch"
    assert ResonanceCalculator.W_I == cfg["W_I"], f"W_I mismatch"
    assert ResonanceCalculator.W_E == cfg["W_E"], f"W_E mismatch"
    assert ResonanceCalculator.F_0 == cfg["F_0"], f"F_0 mismatch"
    assert ResonanceCalculator.TRANSITION_START == cfg["TRANSITION_START"], f"TRANSITION_START mismatch"
    assert ResonanceCalculator.TRANSITION_END == cfg["TRANSITION_END"], f"TRANSITION_END mismatch"


def test_detector_thresholds_match_config():
    """Verify EmergenceDetector class constants match DEFAULT_CONFIG.paper_params.detector"""
    cfg = DEFAULT_CONFIG["paper_params"]["detector"]
    assert EmergenceDetector.THRESHOLD_NONE == cfg["THRESHOLD_NONE"], f"THRESHOLD_NONE mismatch"
    assert EmergenceDetector.THRESHOLD_PRELIMINARY == cfg["THRESHOLD_PRELIMINARY"], f"THRESHOLD_PRELIMINARY mismatch"
    assert EmergenceDetector.THRESHOLD_MODERATE == cfg["THRESHOLD_MODERATE"], f"THRESHOLD_MODERATE mismatch"
    assert EmergenceDetector.THRESHOLD_DEEP == cfg["THRESHOLD_DEEP"], f"THRESHOLD_DEEP mismatch"


def test_weights_sum_to_one():
    """Verify W_K + W_C + W_I + W_E == 1.0"""
    total = ResonanceCalculator.W_K + ResonanceCalculator.W_C + ResonanceCalculator.W_I + ResonanceCalculator.W_E
    assert abs(total - 1.0) < 1e-9, f"Weights sum to {total}, expected 1.0"


def test_threshold_monotonic():
    """Verify detection thresholds are monotonically increasing"""
    thresholds = [
        EmergenceDetector.THRESHOLD_NONE,
        EmergenceDetector.THRESHOLD_PRELIMINARY,
        EmergenceDetector.THRESHOLD_MODERATE,
        EmergenceDetector.THRESHOLD_DEEP,
    ]
    for i in range(len(thresholds) - 1):
        assert thresholds[i] < thresholds[i + 1], f"Threshold not monotonic at index {i}: {thresholds[i]} >= {thresholds[i+1]}"


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
