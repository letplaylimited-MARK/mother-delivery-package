"""QCM Pipeline Engine — 22 公式集成管線 + Cap-D/G 整合"""
import sys, os, math, random, time, logging
from dataclasses import dataclass, field
from typing import Optional

from qcm.core import (
    SimpleRole, create_demo_roles, create_8_roles, ROLE_CONFIG, RoleFactory,
    DeltaSyncer, VectorClock, ResonanceCalculator, EmergenceDetector,
)

from qcm.config import QCMConfig, load_config
from qcm.plugin import plugin_registry, PluginRegistry

logger = logging.getLogger(__name__)


@dataclass
class RoundResult:
    round: int
    R: float
    level: str
    components: dict
    enhanced: dict = field(default_factory=dict)
    emergence_occurred: bool = False
    r_at_emergence: float = 0.0


@dataclass
class PipelineReport:
    total_rounds: int
    emergence_occurred: bool
    r_at_emergence: float
    max_R: float
    avg_R: float
    final_R: float
    rounds: list
    config: dict


class PipelineEngine:
    def __init__(self, config=None):
        self.config = config if config else QCMConfig()
        random.seed(self.config.seed)

        self.round_count = 0
        self.r_at_emergence = 0.0
        self.emergence_occurred = False
        self.rounds_log = []
        self.max_log_size = 100

        self._init_roles()
        self._init_core()
        self._init_plugins()
        self._init_capabilities()
        self._init_paper_modules()

    def _init_roles(self):
        if len(self.config.role_names) == 2:
            self.role_a, self.role_b = create_demo_roles(seed=self.config.seed)
        else:
            roles = RoleFactory.create_role_set(self.config.role_names, base_seed=self.config.seed)
            self.role_a, self.role_b = roles[0], roles[1]
            self._extra_roles = roles[2:]
        self.role_a.interaction_count = 15
        self.role_b.interaction_count = 15

    def _init_core(self):
        self.delta_syncer = DeltaSyncer()
        self.vector_clock = VectorClock("system")
        self.calculator = ResonanceCalculator()
        self.detector = EmergenceDetector()
        self.delta_log = []
        self.vc_log = []
        self.r_components_log = []

    def _init_plugins(self):
        self.plugins = {}
        plugin_registry.enable_by_config(self.config)
        for spec in plugin_registry.execution_list():
            try:
                if spec.name == "epr":
                    inst = spec.instantiate(dimension=4)
                else:
                    inst = spec.instantiate()
                self.plugins[spec.name] = inst
            except Exception as e:
                logger.warning("Plugin %s init failed: %s", spec.name, e)

    def _init_capabilities(self):
        self.crypto = None
        self.healer = None
        if self.config.get("capabilities.crypto", False):
            try:
                from qcm.capabilities import CryptoEngine
                self.crypto = CryptoEngine()
                logger.info("Cap-D CryptoEngine enabled")
            except Exception as e:
                logger.warning("Cap-D init failed: %s", e)
        if self.config.get("capabilities.healer", False):
            try:
                from qcm.capabilities import SelfHealer
                self.healer = SelfHealer()
                logger.info("Cap-G SelfHealer enabled")
            except Exception as e:
                logger.warning("Cap-G init failed: %s", e)

    def _init_paper_modules(self):
        self.modules_enabled = self.config.get("modules", True)
        if not self.modules_enabled:
            self.meeting = None
            self.sandbox = None
            self.flywheel = None
            self.summoning = None
            return
        from qcm.collaboration import MeetingOrchestrator, AuditLog
        from qcm.summoning import DynamicRoleRegistry
        self.meeting = MeetingOrchestrator()
        self.audit_log = AuditLog()
        self.skill_registry = DynamicRoleRegistry()
        self.paper_modules_initialized = True

    def run_round(self):
        self.round_count += 1
        enhanced = {}

        old_state_a = self.role_a.get_state()
        self._role_work(self.role_a)
        new_state_a = self.role_a.get_state()

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

        if self.crypto:
            try:
                cipher = self.crypto.encrypt(str(delta.changed_fields).encode())
                enhanced['crypto'] = {
                    'cipher_len': len(cipher.ciphertext),
                    'nonce': cipher.nonce.hex()[:8],
                    'tag': cipher.tag.hex()[:8],
                }
            except Exception as e:
                enhanced['crypto'] = {'error': str(e)}

        self.vector_clock.increment()
        self.vc_log.append(self.vector_clock.to_dict())

        if 'epr' in self.plugins:
            try:
                inst = self.plugins['epr']
                ent_state = inst.calculate_entanglement(
                    self.role_a.embedding, self.role_b.embedding
                )
                enhanced['epr'] = {
                    'entanglement': round(ent_state.entanglement, 4),
                    'is_entangled': ent_state.is_entangled,
                }
            except Exception as e:
                enhanced['epr'] = {'error': str(e)}

        if 'mdist' in self.plugins:
            try:
                inst = self.plugins['mdist']
                embedding_a = self.role_a.embedding
                embedding_b = self.role_b.embedding
                m_dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(embedding_a, embedding_b)))
                cl = inst.calculate([m_dist], [m_dist * 4])
                enhanced['mahalanobis'] = {
                    'distance': round(m_dist, 4),
                    'contrastive_loss': round(cl, 4),
                }
            except Exception as e:
                enhanced['mahalanobis'] = {'error': str(e)}

        R = self.calculator.calculate_R(self.role_a, self.role_b, round_count=self.round_count)
        components = self.calculator.get_components(self.role_a, self.role_b, round_count=self.round_count)
        self.r_components_log.append(components)
        if len(self.r_components_log) > self.max_log_size:
            self.r_components_log.pop(0)

        if 'dw' in self.plugins:
            try:
                inst = self.plugins['dw']
                inst.add_r_value(R)
                dw = inst.update_weights()
                current_weights = {
                    'w_k': round(dw.w_k, 4), 'w_c': round(dw.w_c, 4),
                    'w_i': round(dw.w_i, 4), 'w_e': round(dw.w_e, 4),
                }
                enhanced['dw'] = current_weights
            except Exception as e:
                enhanced['dw'] = {'error': str(e)}

        if 'deadlock' in self.plugins:
            try:
                inst = self.plugins['deadlock']
                inst.add_r_value(R)
                diversity = max(0.1, 0.8 - 0.01 * self.round_count)
                inst.add_diversity(diversity)
                status = inst.get_status()
                enhanced['deadlock'] = {
                    'score': round(status['deadlock_score'], 3),
                    'warning': status['is_warning'],
                    'deadlock': status['is_deadlock'],
                }
            except Exception as e:
                enhanced['deadlock'] = {'error': str(e)}

        if 'rcs' in self.plugins:
            try:
                inst = self.plugins['rcs']
                r_values = self.calculator.history[-5:] if len(self.calculator.history) >= 5 else self.calculator.history
                metrics = {'K_sim': components['K_sim'], 'C_comp': components['C_comp'], 'I_freq': components['I_freq']}
                rcs_result = inst.calculate_rcs(r_values, [1, 1], metrics)
                enhanced['rcs'] = {
                    'score': round(rcs_result.rcs_score, 4),
                    'decision': rcs_result.decision,
                }
            except Exception as e:
                enhanced['rcs'] = {'error': str(e)}

        self.detector.add_R(R)
        level = self.detector.detect_level()

        if 'flywheel' in self.plugins:
            try:
                inst = self.plugins['flywheel']
                loss = 1.0 - R
                inst.add_loss(loss)
                gradient = R - self.config.emergence_threshold
                fw_state = inst.update(gradient=gradient)
                enhanced['flywheel'] = {
                    'learning_rate': round(inst.learning_rate_history[-1], 4) if inst.learning_rate_history else 0,
                    'acceleration': round(inst.acceleration_history[-1], 4) if inst.acceleration_history else 0,
                    'theta': round(inst.theta, 4),
                    'energy': round(fw_state.energy, 4),
                }
            except Exception as e:
                enhanced['flywheel'] = {'error': str(e)}

        if 'kgrowth' in self.plugins:
            try:
                inst = self.plugins['kgrowth']
                inst.add_interaction(experience_gain=R, synergy_gain=components['C_comp'] + components['I_freq'])
                kg_state = inst.update()
                enhanced['kgrowth'] = {
                    'knowledge': round(kg_state.knowledge, 4),
                    'growth_rate': round(kg_state.growth_rate, 4),
                    'total_nodes': kg_state.total_nodes,
                }
            except Exception as e:
                enhanced['kgrowth'] = {'error': str(e)}

        if 'sandbox' in self.plugins:
            enhanced['sandbox'] = {
                'level': 'micro',
                'srs_score': 0.95,
                'status': 'simulated',
            }

        if 'router' in self.plugins:
            try:
                from qcm.decision import InputFeatures
                inst = self.plugins['router']
                features = InputFeatures(
                    complexity=components['E_div'],
                    has_rules=self.round_count > 10,
                    has_examples=True,
                    uncertainty=1.0 - R,
                    time_constraint=0.5,
                )
                decision = inst.route(features)
                enhanced['router'] = {
                    'type': decision.reasoning_type.value,
                    'confidence': round(decision.confidence, 4),
                }
            except Exception as e:
                enhanced['router'] = {'error': str(e)}

        if 'pareto' in self.plugins:
            try:
                from qcm.decision import Option
                inst = self.plugins['pareto']
                opt1 = Option(id="sync", cost=0.1 * (1 - R), benefit=R, risk=1 - R, time=1.0)
                opt2 = Option(id="wait", cost=0.05, benefit=R * 0.7, risk=0.3, time=2.0)
                inst.add_option(opt1)
                inst.add_option(opt2)
                pareto_results = inst.analyze()
                if pareto_results:
                    best = min(pareto_results, key=lambda x: x.score)
                    enhanced['pareto'] = {
                        'best_option': best.option_id,
                        'score': round(best.score, 4),
                        'is_pareto_optimal': best.is_pareto_optimal,
                    }
            except Exception as e:
                enhanced['pareto'] = {'error': str(e)}

        self._role_receive(self.role_b, delta)
        self._update_alignment()

        if self.healer:
            try:
                if self.round_count % max(1, self.config.get("capabilities.healer_interval", 10)) == 0:
                    snapshot = self.healer.create_snapshot({
                        'round': self.round_count,
                        'R': R,
                        'role_a_embedding': self.role_a.embedding,
                        'role_b_embedding': self.role_b.embedding,
                    })
                    enhanced['healer'] = {
                        'snapshot_id': snapshot.snapshot_id.hex()[:8],
                        'round': self.round_count,
                        'R': round(R, 4),
                    }
                elif R < self.config.get("capabilities.healer_restore_threshold", 0.5):
                    self.healer.restore_latest()
                    enhanced['healer'] = {'restored': True, 'R_before': round(R, 4)}
            except Exception as e:
                enhanced['healer'] = {'error': str(e)}

        paper_enhanced = self._run_paper_modules(R, components)
        enhanced.update(paper_enhanced)

        is_emergence = self.detector.is_emergence()
        if is_emergence and not self.emergence_occurred:
            self.emergence_occurred = True
            self.r_at_emergence = R
            logger.info("EMERGENCE at R=%.4f (round %d)", R, self.round_count)

        result = RoundResult(
            round=self.round_count,
            R=round(R, 4),
            level=level,
            components=components,
            enhanced=enhanced,
            emergence_occurred=self.emergence_occurred,
            r_at_emergence=self.r_at_emergence,
        )
        self.rounds_log.append(result)
        if len(self.rounds_log) > self.max_log_size:
            self.rounds_log.pop(0)

        return result

    def _run_paper_modules(self, R, components):
        enhanced = {}
        if not getattr(self, 'paper_modules_initialized', False):
            return enhanced
        try:
            self.meeting.add_message("system", f"Round {self.round_count}: R={R:.4f}")
            state = self.meeting.get_state()
            enhanced['meeting'] = {
                'phase': state.current_phase,
                'rounds': state.round_count,
                'is_deadlocked': state.is_deadlocked,
            }
        except Exception as e:
            enhanced['meeting'] = {'error': str(e)}
        try:
            from qcm.sandbox import calculate_srs, confidence_gate
            srs = calculate_srs([R], f_target=0.85)
            enhanced['sandbox'] = {'srs': srs, 'can_advance': confidence_gate(srs, 0.85)}
        except Exception as e:
            enhanced['sandbox'] = {'error': str(e)}
        try:
            from qcm.flywheel import total_energy
            fw_energy = total_energy(E_resonance=R, E_flywheel=0.1 * self.round_count)
            enhanced['flywheel'] = {'total_energy': round(fw_energy, 4)}
        except Exception as e:
            enhanced['flywheel'] = {'error': str(e)}
        return enhanced

    def _role_work(self, role):
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

    def _role_receive(self, role, delta):
        role.add_memory({"type": "receive", "delta": delta.changed_fields, "round": self.round_count})
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

    def get_report(self):
        if not self.rounds_log:
            return None
        R_vals = [r.R for r in self.rounds_log]
        return PipelineReport(
            total_rounds=self.round_count,
            emergence_occurred=self.emergence_occurred,
            r_at_emergence=self.r_at_emergence,
            max_R=max(R_vals),
            avg_R=sum(R_vals) / len(R_vals),
            final_R=R_vals[-1],
            rounds=self.rounds_log,
            config=self.config.to_dict(),
        )

    def run(self, max_rounds=None):
        if max_rounds is None:
            max_rounds = self.config.max_rounds
        for _ in range(max_rounds):
            result = self.run_round()
            if self.emergence_occurred and self.config.mode == "production":
                pass
        return self.get_report()
