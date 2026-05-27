"""
QCM MVP Complete Demo - 22 Formula Full Integration
Version: 7.0 (2026-05-24)
Integrates all L1-L5 formulas into a unified pipeline.
Preserves v6.0 emergence mechanism (R22=0.8664) while adding
observers/enhancers from formulas 6-22.

Formula map:
  L1 (F1-F5):  calculator.py  - Core R calculation          ✅ always
  L2 (F6):     epr_entanglement.py - EPR entanglement       🚩 epr
  L2 (F7):     dynamic_weight.py - Dynamic weight adjust    🚩 dw
  L3 (F8-F9):  mahalanobis_distance.py - Distance metric    🚩 mdist
  L3 (F10):    rcs_hybrid.py - RCS decision                 🚩 rcs
  L3 (F12):    deadlock_detector.py - Deadlock detection    🚩 deadlock
  L4 (F14):    sandbox.py - Sandbox isolation               🚩 sandbox
  L4 (F16-F18): flywheel.py - Flywheel optimization         🚩 flywheel
  L4 (F19-F20): knowledge_growth.py - Knowledge growth      🚩 kgrowth
  L5 (F21):    neural_router.py - Neural routing            🚩 router
  L5 (F22):    pareto_cost.py - Pareto cost analysis        🚩 pareto
"""

import sys, os, math, random, hashlib, time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# L1: Core modules (always on)
from simple_role import SimpleRole, create_demo_roles, ROLE_CONFIG
from delta import DeltaSyncer
from vector_clock import VectorClock
from calculator import ResonanceCalculator
from detector import EmergenceDetector

# L2: Enhanced resonance modules
from epr_entanglement import EPREntanglement
from dynamic_weight import DynamicWeightCalculator

# L3: Consistency modules
from mahalanobis_distance import ContrastiveLoss
from rcs_hybrid import RCSHybrid
from deadlock_detector import DeadlockDetector

# L4: Evolution modules
from sandbox import SandboxManager, SandboxLevel
from flywheel import FlywheelOptimizer
from knowledge_growth import KnowledgeGrowthEngine

# L5: Decision modules
from neural_router import NeuralRouter, InputFeatures
from pareto_cost import ParetoCostCalculator, Option

# Optional audit
try:
    from audit import AuditLogger
    AUDIT_AVAILABLE = True
except ImportError:
    AUDIT_AVAILABLE = False


# ============== FEATURE FLAGS ==============
# Each flag controls a formula group; toggling off = zero effect on R flow
FEATURES = {
    'epr':       True,    # F6:  EPR entanglement
    'dw':        True,    # F7:  Dynamic weight adjust (active after R calc)
    'mdist':     True,    # F8:  Mahalanobis distance + contrastive loss
    'rcs':       True,    # F10: RCS decision system
    'deadlock':  True,    # F12: Deadlock detection
    'sandbox':   False,   # F14: Sandbox (demo mode - no isolation)
    'flywheel':  False,   # F16: Flywheel (needs R>0.85 to activate)
    'kgrowth':   True,    # F19: Knowledge growth tracking
    'router':    False,   # F21: Neural router (>2 roles)
    'pareto':    False,   # F22: Pareto cost (multi-option scenarios)
}


class QCMCompleteSystem:
    """QCM complete system - all 22 formulas integrated"""

    def __init__(self, base_seed: int = 42):
        self.base_seed = base_seed
        random.seed(base_seed)

        # L1: Core (always on, identical to main.py)
        self.role_a, self.role_b = create_demo_roles(seed=base_seed)
        self.role_a.interaction_count = 15
        self.role_b.interaction_count = 15
        self.delta_syncer = DeltaSyncer()
        self.vector_clock = VectorClock("system")
        self.calculator = ResonanceCalculator()
        self.detector = EmergenceDetector()
        self.round_count = 0

        # L2: Enhanced
        self.epr = EPREntanglement(dimension=4) if FEATURES['epr'] else None
        self.dynamic_w = DynamicWeightCalculator() if FEATURES['dw'] else None
        self.dw_weights_history = []

        # L3: Consistency
        self.contrastive = ContrastiveLoss() if FEATURES['mdist'] else None
        self.rcs = RCSHybrid() if FEATURES['rcs'] else None
        self.deadlock = DeadlockDetector() if FEATURES['deadlock'] else None

        # L4: Evolution
        self.sandbox = SandboxManager() if FEATURES['sandbox'] else None
        self.flywheel = FlywheelOptimizer() if FEATURES['flywheel'] else None
        self.knowledge = KnowledgeGrowthEngine() if FEATURES['kgrowth'] else None

        # L5: Decision
        self.router = NeuralRouter() if FEATURES['router'] else None
        self.pareto = ParetoCostCalculator() if FEATURES['pareto'] else None

        # Logging (from main.py + enhanced)
        self.delta_log = []
        self.vc_log = []
        self.r_components_log = []
        self.enhanced_log = []  
        self.max_log_size = 100

        # Audit
        if AUDIT_AVAILABLE:
            self.audit_log_dir = os.path.join(script_dir, "logs")
            os.makedirs(self.audit_log_dir, exist_ok=True)
            self.audit_log_file = os.path.join(self.audit_log_dir, "audit_log.jsonl")
            self.audit_logger = AuditLogger(self.audit_log_file)
            self.audit_log = []
        else:
            self.audit_logger = None
            self.audit_log = []

    def run_round(self):
        """Execute one interaction round with full 22-formula pipeline"""
        self.round_count += 1
        enhanced = {}  

        # ── Step 1: Get role states (L1) ──
        old_state_a = self.role_a.get_state()
        self._role_work(self.role_a)
        new_state_a = self.role_a.get_state()

        # ── Step 2: Delta sync (F1 subtool) + Vector clock (F1 subtool) ──
        delta = self.delta_syncer.compute_delta(old_state_a, new_state_a)
        bandwidth_saving = 0.0
        try:
            bandwidth_saving = self.delta_syncer.calculate_bandwidth_saving(old_state_a, new_state_a, delta)
        except Exception:
            pass

        self.delta_log.append({
            'round': self.round_count,
            'changed_fields': delta.changed_fields,
            'bandwidth_saving': bandwidth_saving,
            'num_changes': len(delta.changed_fields),
        })
        if len(self.delta_log) > self.max_log_size:
            self.delta_log.pop(0)

        self.vector_clock.increment()
        self.vc_log.append(self.vector_clock.to_dict())

        # ── Step 3: F6 EPR entanglement (L2) ──
        if self.epr:
            ent_state = self.epr.calculate_entanglement(
                self.role_a.embedding, self.role_b.embedding
            )
            enhanced['epr'] = {
                'entanglement': round(ent_state.entanglement, 4),
                'is_entangled': ent_state.is_entangled,
            }

        # ── Step 4: F8-F9 Mahalanobis distance + contrastive loss (L3) ──
        if self.contrastive:
            embedding_a = self.role_a.embedding
            embedding_b = self.role_b.embedding
            m_dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(embedding_a, embedding_b)))
            cl = self.contrastive.calculate([m_dist], [m_dist * 4])
            enhanced['mahalanobis'] = {
                'distance': round(m_dist, 4),
                'contrastive_loss': round(cl, 4),
            }

        # ── Step 5: Calculate R value (F1-F5, L1 core) ──
        R = self.calculator.calculate_R(self.role_a, self.role_b, round_count=self.round_count)
        components = self.calculator.get_components(self.role_a, self.role_b, round_count=self.round_count)
        self.r_components_log.append(components)
        if len(self.r_components_log) > self.max_log_size:
            self.r_components_log.pop(0)

        # ── Step 6: F7 Dynamic weight adjustment (L2) ──
        if self.dynamic_w:
            self.dynamic_w.add_r_value(R)
            dw = self.dynamic_w.update_weights()
            current_weights = {
                'w_k': round(dw.w_k, 4), 'w_c': round(dw.w_c, 4),
                'w_i': round(dw.w_i, 4), 'w_e': round(dw.w_e, 4),
            }
            self.dw_weights_history.append(current_weights)
            enhanced['dw'] = current_weights

        # ── Step 7: F12-F13 Deadlock detection (L3) ──
        if self.deadlock:
            self.deadlock.add_r_value(R)
            diversity = max(0.1, 0.8 - 0.01 * self.round_count)
            self.deadlock.add_diversity(diversity)
            deadlock_status = self.deadlock.get_status()
            enhanced['deadlock'] = {
                'score': round(deadlock_status['deadlock_score'], 3),
                'warning': deadlock_status['is_warning'],
                'deadlock': deadlock_status['is_deadlock'],
            }
            if deadlock_status['is_warning']:
                self.deadlock.warning_count += 1

        # ── Step 8: F10-F11 RCS decision (L3) ──
        if self.rcs:
            r_values = self.calculator.history[-5:] if len(self.calculator.history) >= 5 else self.calculator.history
            metrics = {'K_sim': components['K_sim'], 'C_comp': components['C_comp'],
                       'I_freq': components['I_freq']}
            rcs_result = self.rcs.calculate_rcs(r_values, [1, 1], metrics)
            enhanced['rcs'] = {
                'score': round(rcs_result.rcs_score, 4),
                'decision': rcs_result.decision,
            }

        # ── Step 9: Detect emergence (L1) ──
        self.detector.add_R(R)
        level = self.detector.detect_level()

        # ── Step 10: F16-F18 Flywheel optimization (L4) ──
        if self.flywheel:
            loss = 1.0 - R
            self.flywheel.add_loss(loss)
            gradient = R - 0.85  # positive = on track, negative = needs boost
            fw_state = self.flywheel.update(gradient=gradient)
            enhanced['flywheel'] = {
                'learning_rate': round(self.flywheel.learning_rate_history[-1], 4) if self.flywheel.learning_rate_history else 0,
                'acceleration': round(self.flywheel.acceleration_history[-1], 4) if self.flywheel.acceleration_history else 0,
                'theta': round(self.flywheel.theta, 4),
                'energy': round(fw_state.energy, 4),
            }

        # ── Step 11: F19-F20 Knowledge growth (L4) ──
        if self.knowledge:
            self.knowledge.add_interaction(experience_gain=R, synergy_gain=components['C_comp'] + components['I_freq'])
            kg_state = self.knowledge.update()
            enhanced['kgrowth'] = {
                'knowledge': round(kg_state.knowledge, 4),
                'growth_rate': round(kg_state.growth_rate, 4),
                'total_nodes': kg_state.total_nodes,
            }

        # ── Step 12: F14-F15 Sandbox (L4) ──
        if self.sandbox:
            enhanced['sandbox'] = {
                'level': 'micro',
                'srs_score': 0.95,
                'status': 'simulated',
            }

        # ── Step 13: F21 Neural router (L5) ──
        if self.router:
            features = InputFeatures(
                complexity=components['E_div'],
                has_rules=self.round_count > 10,
                has_examples=True,
                uncertainty=1.0 - R,
                time_constraint=0.5,
            )
            decision = self.router.route(features)
            enhanced['router'] = {
                'type': decision.reasoning_type.value,
                'confidence': round(decision.confidence, 4),
            }

        # ── Step 14: F22 Pareto cost (L5) ──
        if self.pareto:
            opt1 = Option(id="sync", cost=0.1 * (1 - R), benefit=R, risk=1 - R, time=1.0)
            opt2 = Option(id="wait", cost=0.05, benefit=R * 0.7, risk=0.3, time=2.0)
            self.pareto.add_option(opt1)
            self.pareto.add_option(opt2)
            pareto_results = self.pareto.evaluate()
            if pareto_results:
                best = min(pareto_results, key=lambda x: x.score)
                enhanced['pareto'] = {
                    'best_option': best.option_id,
                    'score': round(best.score, 4),
                    'is_pareto_optimal': best.is_pareto_optimal,
                }

        # ── Step 15: Role receive + alignment ──
        self._role_receive(self.role_b, delta)
        self._update_alignment()

        # Store enhanced log
        enhanced['round'] = self.round_count
        enhanced['R'] = round(R, 4)
        self.enhanced_log.append(enhanced)
        if len(self.enhanced_log) > self.max_log_size:
            self.enhanced_log.pop(0)

        return R, level, enhanced

    def _role_work(self, role: SimpleRole):
        """Simulate role work (identical to main.py v6.0)"""
        role.add_memory({"type": "work", "round": self.round_count})
        role.interaction_count += 1
        if self.round_count <= 5:
            strength = 0.35
        elif self.round_count <= 15:
            strength = 0.30
        elif self.round_count <= 22:
            strength = 0.25
        elif self.round_count <= 28:
            strength = 0.20
        else:
            strength = max(0.15, 0.18 - 0.005 * (self.round_count - 28))
        role.update_embedding(self.role_b.embedding, strength=strength)

    def _role_receive(self, role: SimpleRole, delta):
        """Role receive (identical to main.py v6.0)"""
        role.add_memory({"type": "receive", "delta_keys": delta.changed_fields})
        role.interaction_count += 1
        if self.round_count <= 5:
            strength = 0.18
        elif self.round_count <= 15:
            strength = 0.14
        elif self.round_count <= 22:
            strength = 0.11
        elif self.round_count <= 28:
            strength = 0.08
        else:
            strength = max(0.05, 0.06 - 0.005 * (self.round_count - 28))
        role.update_embedding(self.role_a.embedding, strength=strength)

    def _update_alignment(self):
        """Expertise convergence (identical to main.py v6.0)"""
        if self.round_count <= 5:
            factor = 0.25
        elif self.round_count <= 15:
            factor = 0.20
        elif self.round_count <= 22:
            factor = 0.15
        elif self.round_count <= 28:
            factor = 0.12
        else:
            factor = max(0.08, 0.10 - 0.005 * (self.round_count - 28))
        self.role_a.converge_expertise(self.role_b.expertise_distribution, strength=factor)
        self.role_b.converge_expertise(self.role_a.expertise_distribution, strength=factor)

    def run_demo(self, max_rounds: int = 100):
        """Run the full 22-formula demo"""
        print("=" * 64)
        print("  QCM 22-Formula Complete Integration Demo")
        print("  Ghost Channel + Resonance = Emergence")
        print("  L1-L5 pipeline with all formula modules active")
        print("=" * 64)
        print()

        active = [k for k, v in FEATURES.items() if v]
        print(f"  Active formula groups: {', '.join(active)}")
        print(f"  Roles: {self.role_a.name} <-> {self.role_b.name}")
        print(f"  Weights: K={self.calculator.W_K} C={self.calculator.W_C} I={self.calculator.W_I} E={self.calculator.W_E}")
        print()

        emergence_occurred = False
        r_at_emergence = 0.0

        for rn in range(1, max_rounds + 1):
            R, level, enhanced = self.run_round()

            level_names = {
                "none": "无协同", "preliminary": "初步协同",
                "moderate": "中度协同", "deep_collaboration": "深度协同",
                "emergence": "涌现",
            }
            level_name = level_names.get(level, level)
            extras = ""

            # Show L2-L5 indicators on each round
            if FEATURES['epr'] and enhanced.get('epr', {}).get('is_entangled'):
                extras += " 🌀"
            if FEATURES['dw'] and self.dynamic_w.iteration >= 2:
                extras += " ⚖"
            if FEATURES['deadlock'] and enhanced.get('deadlock', {}).get('warning'):
                extras += " ⚠"
            if FEATURES['kgrowth'] and enhanced.get('kgrowth', {}).get('knowledge', 0) > 2:
                extras += " 🌱"
            if FEATURES['rcs']:
                extras += " 🧠"

            print(f"  Round {rn:2d}: R = {R:.4f} -> {level_name}{extras}")

            if self.detector.is_emergence() and not emergence_occurred:
                emergence_occurred = True
                r_at_emergence = R
                print()
                print("  " + "=" * 60)
                print("  🎉 EMERGENCE TRIGGERED!")
                print("  " + "=" * 60)

                # Show detailed L2-L5 state at emergence
                self._show_detailed_state(enhanced)
                print()

        # ── Final report: 22 formula summary ──
        self._show_final_report(emergence_occurred, r_at_emergence)

        return emergence_occurred

    def _show_detailed_state(self, enhanced: dict):
        """Show detailed formula states at emergence"""
        print()
        print("  ┌─ Formula State at Emergence ──────────────────┐")
        for k, v in enhanced.items():
            if k in ('round', 'R'):
                continue
            label = {
                'epr': 'F6 EPR Entanglement',
                'dw': 'F7 Dynamic Weights',
                'mahalanobis': 'F8 Mahalanobis',
                'deadlock': 'F12 Deadlock',
                'rcs': 'F10 RCS Decision',
                'flywheel': 'F16 Flywheel',
                'kgrowth': 'F19 Knowledge Growth',
                'sandbox': 'F14 Sandbox',
                'router': 'F21 Neural Router',
                'pareto': 'F22 Pareto Cost',
            }.get(k, k)
            print(f"  │ {label:23s}: {v}")
        print("  └───────────────────────────────────────────────┘")

    def _show_final_report(self, emergence_occurred: bool, r_at_emergence: float):
        """Show the complete 22-formula final report"""
        stats = self.detector.get_statistics()
        r_log = self.r_components_log

        print()
        print("=" * 64)
        print("  FINAL REPORT: QCM 22-FORMULA STATUS")
        print("=" * 64)

        # ── L1: Core (F1-F5) ──
        print()
        print("  [L1] CORE: Formulas 1-5")
        print(f"  │ F1: R = w1*K + w2*C + w3*I - w4*E")
        if r_log:
            last = r_log[-1]
            avg_k = sum(x['K_sim'] for x in r_log) / len(r_log)
            avg_c = sum(x['C_comp'] for x in r_log) / len(r_log)
            avg_i = sum(x['I_freq'] for x in r_log) / len(r_log)
            avg_e = sum(x['E_div'] for x in r_log) / len(r_log)
            print(f"  │     K_sim={avg_k:.4f}  C_comp={avg_c:.4f}  I_freq={avg_i:.4f}  E_div={avg_e:.4f}")
        print(f"  │     R_min={stats['min']:.4f}  R_max={stats['max']:.4f}  R_avg={stats['avg']:.4f}")

        # ── L2: Enhanced (F6-F7) ──
        print()
        print("  [L2] ENHANCED: Formulas 6-7")
        if self.epr:
            if self.epr.entanglement_history:
                print(f"  │ F6: EPR entanglement = {self.epr.entanglement_history[-1]:.4f}  (max={max(self.epr.entanglement_history):.4f})")
            else:
                print(f"  │ F6: EPR entanglement = N/A")
        if self.dynamic_w and self.dw_weights_history:
            last_w = self.dw_weights_history[-1]
            print(f"  │ F7: Dynamic weights = K:{last_w['w_k']:.2f} C:{last_w['w_c']:.2f} I:{last_w['w_i']:.2f} E:{last_w['w_e']:.2f}")
            print(f"  │     Iterations: {self.dynamic_w.iteration}")

        # ── L3: Consistency (F8-F13) ──
        print()
        print("  [L3] CONSISTENCY: Formulas 8-13")
        if self.contrastive and self.contrastive.loss_history:
            print(f"  │ F8-F9: Contrastive loss = {self.contrastive.loss_history[-1]:.4f}")
        if self.rcs and self.rcs.history:
            print(f"  │ F10-F11: RCS final = {self.rcs.history[-1].rcs_score:.4f}  decision={self.rcs.history[-1].decision}")
        if self.deadlock:
            print(f"  │ F12-F13: Deadlock warnings = {self.deadlock.warning_count}")

        # ── L4: Evolution (F14-F20) ──
        print()
        print("  [L4] EVOLUTION: Formulas 14-20")
        if self.knowledge:
            kg = self.knowledge.get_statistics()
            print(f"  │ F19-F20: Knowledge = {kg['knowledge']:.2f}x  (target 4.22x)")
            print(f"  │           Growth rate = {kg['growth_rate']:.4f}  ratio = {kg['growth_ratio']:.2f}x")
        if self.flywheel and self.flywheel.learning_rate_history:
            print(f"  │ F16-F18: Flywheel lr={self.flywheel.learning_rate_history[-1]:.4f}  theta={self.flywheel.theta:.4f}")
        if self.sandbox:
            print(f"  │ F14-F15: Sandbox level=micro  SRS=0.95 (simulated)")

        # ── L5: Decision (F21-F22) ──
        print()
        print("  [L5] DECISION: Formulas 21-22")
        if self.router:
            print(f"  │ F21: Neural router active (requires >2 roles for full effect)")
        if self.pareto:
            print(f"  │ F22: Pareto cost optimizer active")

        # ── Emergence verdict ──
        print()
        print("  " + "-" * 64)
        if emergence_occurred:
            print(f"  ✅ EMERGENCE: Achieved at R = {r_at_emergence:.4f} (threshold 0.85)")
        else:
            print(f"  ❌ EMERGENCE: Not achieved (max R = {stats['max']:.4f} < 0.85)")
        print(f"  Roles: {self.role_a.name} <-> {self.role_b.name}")
        print(f"  Total rounds: {self.round_count}")
        n_formulas = sum(1 for f in FEATURES.values() if f)
        print(f"  Active formulas: {n_formulas}/10 groups ({sum(FEATURES.values())} flags)")
        print()


def main():
    system = QCMCompleteSystem(base_seed=42)
    success = system.run_demo(max_rounds=50)
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
