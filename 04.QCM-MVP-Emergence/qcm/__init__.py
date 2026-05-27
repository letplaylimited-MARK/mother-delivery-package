"""QCM 統一命名空間包 — 論文 5 大模組全整合"""
import sys, os

_code_dir = os.path.join(os.path.dirname(__file__), '..', '02-代码编写')
if os.path.isdir(_code_dir) and _code_dir not in sys.path:
    sys.path.insert(0, os.path.abspath(_code_dir))

from qcm.config import QCMConfig, load_config
from qcm.plugin import PluginRegistry, plugin_registry
from qcm.pipeline import PipelineEngine
from qcm.roles import ROLE_REGISTRY, weighted_consensus
from qcm.collaboration import MEETING_PHASES, MeetingOrchestrator, VoteMode, detect_deadlock, AuditLog
from qcm.sandbox import SANDBOX_LAYERS, calculate_srs, confidence_gate, priority_score
from qcm.flywheel import total_energy, lyapunov_function, adaptive_learning_rate
from qcm.summoning import extract_tfidf_keywords, calculate_skill_match, DynamicRoleRegistry

__all__ = [
    'QCMConfig', 'load_config',
    'PluginRegistry', 'plugin_registry',
    'PipelineEngine',
    'ROLE_REGISTRY', 'weighted_consensus',
    'MEETING_PHASES', 'MeetingOrchestrator', 'VoteMode', 'detect_deadlock', 'AuditLog',
    'SANDBOX_LAYERS', 'calculate_srs', 'confidence_gate', 'priority_score',
    'total_energy', 'lyapunov_function', 'adaptive_learning_rate',
    'extract_tfidf_keywords', 'calculate_skill_match', 'DynamicRoleRegistry',
]
