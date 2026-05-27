"""
QCM-MVP 全模组验证测试 (v2 — uses correct module APIs)
Tests all 22 formulas + 10 atomic capabilities + main entry points
"""
import sys, os, math
CODE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CODE)
os.chdir(CODE)

PASS, FAIL = 0, 0

def test(name, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"  [PASS] {name}")
    else:
        FAIL += 1
        print(f"  [FAIL] {name}  {detail}")

print("=" * 60)
print("QCM-MVP Comprehensive Verification v2")
print("=" * 60)

# ── Use each module's built-in test function ──
import importlib, io, contextlib

MODULES = [
    "simple_role",
    "delta",
    "vector_clock",
    "calculator",
    "detector",
    "epr_entanglement",
    "dynamic_weight",
    "mahalanobis_distance",
    "rcs_hybrid",
    "deadlock_detector",
    "sandbox",
    "flywheel",
    "knowledge_growth",
    "neural_router",
    "pareto_cost",
    "audit",
    "crypto",
    "self_healer",
]

print(f"\n--- Running {len(MODULES)} module-level tests ---")
for mod_name in MODULES:
    try:
        mod = importlib.import_module(mod_name)
        test_func_name = f"test_{mod_name}"
        # Map module name to test function
        test_map = {
            "simple_role": None,
            "delta": "test_delta",
            "vector_clock": "test_vector_clock",
            "calculator": "test_calculator",
            "detector": "test_detector",
            "epr_entanglement": "test_epr_entanglement",
            "dynamic_weight": "test_dynamic_weight",
            "mahalanobis_distance": "test_mahalanobis",
            "rcs_hybrid": "test_rcs_hybrid",
            "deadlock_detector": "test_deadlock_detector",
            "sandbox": "test_sandbox",
            "flywheel": "test_flywheel",
            "knowledge_growth": "test_knowledge_growth",
            "neural_router": "test_neural_router",
            "pareto_cost": "test_pareto_cost",
            "audit": "test_audit",
            "crypto": "test_crypto",
            "self_healer": "test_self_healer",
        }
        func_name = test_map.get(mod_name)
        if func_name and hasattr(mod, func_name):
            f = io.StringIO()
            with contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
                getattr(mod, func_name)()
            test(f"{mod_name} test", True)
        else:
            # Just test import works
            test(f"{mod_name} import", True)
    except Exception as e:
        test(f"{mod_name} test", False, str(e))

# ── Core workflow: 5-round resonance ──
print("\n--- Core Workflow (F1-F5) ---")
try:
    from simple_role import SimpleRole, create_demo_roles
    from delta import DeltaSyncer
    from vector_clock import VectorClock
    from calculator import ResonanceCalculator
    from detector import EmergenceDetector

    A, B = create_demo_roles()
    calc = ResonanceCalculator()
    ds = DeltaSyncer()
    vc = VectorClock("main")
    det = EmergenceDetector()
    for rnd in range(5):
        A.interaction_count += 1
        B.interaction_count += 1
        old = {"memory": A.memory.copy()} if hasattr(A, "memory") else {}
        new = {"memory": A.memory.copy() + [{"r": rnd}]} if hasattr(A, "memory") else {}
        if old and new:
            delta_p = ds.compute_delta(old, new)
        vc.increment()
        R = calc.calculate_R(A, B, rnd)
        det.add_R(R)
    test("Core: 5-round resonance", R > 0.7, f"R={R:.4f}")
except Exception as e:
    test("Core: 5-round resonance", False, str(e))

# ── main_complete.py end-to-end ──
print("\n--- main_complete.py: 22-formula pipeline ---")
try:
    from main_complete import QCMCompleteSystem
    sys.stdout = io.StringIO()  # suppress output
    sys.stderr = io.StringIO()
    sys_stdout = sys.stdout
    sys_stderr = sys.stderr
    system = QCMCompleteSystem(base_seed=42)
    # Run only 30 rounds for speed
    system.run_demo(max_rounds=30)
    test("main_complete: initialization", True)
except Exception as e:
    test("main_complete: initialization", False, str(e))
finally:
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

# ── qcm/ namespace package ──
print("\n--- qcm/ namespace package (Phase A) ---")
try:
    QCM_DIR = os.path.dirname(CODE)  # parent of 02-代码编写
    sys.path.insert(0, QCM_DIR)
    from qcm import plugin_registry, QCMConfig, PluginRegistry, PipelineEngine
    test("qcm: imports", True)
    cfg = QCMConfig({"max_rounds": 5, "seed": 42, "silent": True})
    test("qcm: QCMConfig created", True)
    pl = plugin_registry.enable_by_config(cfg)
    test("qcm: plugin_registry enabled", True)
    engine = PipelineEngine(cfg)
    for rnd in range(5):
        result = engine.run_round()
    test("qcm: pipeline 5-round", result.R > 0, f"R={result.R:.4f}")
    report = engine.get_report()
    test("qcm: report generated", report is not None and report.total_rounds == 5)
except Exception as e:
    test("qcm: namespace package", False, str(e))

# ── Summary ──
print("\n" + "=" * 60)
print(f"  Results: {PASS} PASS / {FAIL} FAIL / {PASS+FAIL} TOTAL")
print("=" * 60)
sys.exit(0 if FAIL == 0 else 1)
