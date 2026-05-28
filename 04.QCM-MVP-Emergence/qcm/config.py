"""QCM 配置系統 — 支援 dict/JSON/YAML 載入"""
import json, os, copy

DEFAULT_CONFIG = {
    "mode": "research",
    "seed": 42,
    "base_seed": 42,
    "roles": ["Secretary", "Researcher"],
    "plugins": {
        "epr": True,
        "dw": True,
        "mdist": True,
        "rcs": True,
        "deadlock": True,
        "kgrowth": True,
        "sandbox": False,
        "flywheel": False,
        "router": False,
        "pareto": False,
    },
    "weights": {"K": 0.35, "C": 0.40, "I": 0.25, "E": 0.0},
    "emergence_threshold": 0.85,
    "max_rounds": 50,
    "logging": {"level": "INFO", "file": None, "dir": "logs"},
    "output": {"dir": "output", "format": "json"},
    "audit": True,

    # ── Phase 2: paper_params — all 14 formula module constants ──
    "paper_params": {
        "calculator": {
            "W_K": 0.35, "W_C": 0.40, "W_I": 0.25, "W_E": 0.00,
            "F_0": 5,
            "TRANSITION_START": 10, "TRANSITION_END": 30,
        },
        "detector": {
            "THRESHOLD_NONE": 0.3, "THRESHOLD_PRELIMINARY": 0.5,
            "THRESHOLD_MODERATE": 0.65, "THRESHOLD_DEEP": 0.85,
        },
        "epr_entanglement": {
            "LAMBDA": 0.1, "ENTANGLEMENT_THRESHOLD": 0.5,
            "STRONG_ENTANGLEMENT": 0.7,
            "MEAN_ENTANGLEMENT": 0.64, "STD_ENTANGLEMENT": 0.12,
            "MIN_ENTANGLEMENT": 0.28, "MAX_ENTANGLEMENT": 0.89,
        },
        "dynamic_weight": {
            "LAMBDA": 0.1, "R_TARGET": 0.85, "K_DECAY": 0.05,
            "INITIAL_WEIGHTS": {"w_k": 0.25, "w_c": 0.35, "w_i": 0.20, "w_e": 0.20},
        },
        "deadlock_detector": {
            "ALPHA_1": 0.30, "ALPHA_2": 0.35, "ALPHA_3": 0.20, "ALPHA_4": 0.15,
            "ETA_N": 2, "ETA_G": 0.5, "ETA_S": 0.01, "DEADLOCK_THRESHOLD": 2.0,
        },
        "flywheel": {
            "ALPHA_INIT": 0.1, "BETA": 0.9, "GAMMA": 0.1, "KAPPA": 0.5,
            "LAMBDA_VAR": 0.1, "ETA": 0.1, "T_REF": 10, "ZETA": 0.7, "RHO_MAX": 0.73,
        },
        "knowledge_growth": {
            "ETA": 0.1, "TARGET_GROWTH": 4.22, "SYNERGY_BETA": 0.91,
        },
        "sandbox": {
            "LAMBDA": 0.5, "MU": 0.2, "SRS_TARGET": 0.9, "SIGMA": 0.1,
        },
        "neural_router": {
            "NEURAL_THRESHOLD": 0.7, "SYMBOLIC_THRESHOLD": 0.3,
            "TIME_CRITICAL_THRESHOLD": 0.8,
        },
        "pareto_cost": {
            "ALPHA": 0.4, "BETA": 0.3, "GAMMA": 0.3,
        },
        "semantic_matcher": {
            "TOP_K": 10, "PRECISION_TARGET": 0.941,
        },
        "predictive_sync": {
            "TARGET_ACCURACY": 0.86, "WINDOW_SIZE": 10,
        },
        "mahalanobis_distance": {
            "MARGIN_POS": 0.5, "MARGIN_NEG": 2.0,
        },
        "rcs_hybrid": {
            "ALPHA": 0.4, "BETA": 0.35, "GAMMA": 0.25, "DECISION_THRESHOLD": 0.7,
        },
    },
}


class QCMConfig:
    def __init__(self, config_dict=None):
        self._data = copy.deepcopy(DEFAULT_CONFIG)
        if config_dict:
            self._deep_update(self._data, config_dict)

    @staticmethod
    def _deep_update(base, overlay):
        for k, v in overlay.items():
            if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                QCMConfig._deep_update(base[k], v)
            else:
                base[k] = v

    @classmethod
    def from_dict(cls, d):
        return cls(d)

    @classmethod
    def from_json(cls, path):
        with open(path, 'r', encoding='utf-8') as f:
            return cls(json.load(f))

    @classmethod
    def from_yaml(cls, path):
        try:
            import yaml
            with open(path, 'r', encoding='utf-8') as f:
                return cls(yaml.safe_load(f))
        except ImportError:
            raise ImportError("PyYAML required for YAML config: pip install pyyaml")

    def get(self, key, default=None):
        keys = key.split('.')
        val = self._data
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k)
            else:
                return default
        return val if val is not None else default

    def set(self, key, value):
        keys = key.split('.')
        target = self._data
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value

    @property
    def active_plugins(self):
        return [k for k, v in self._data['plugins'].items() if v]

    @property
    def role_names(self):
        return self._data['roles']

    @property
    def mode(self):
        return self._data['mode']

    @property
    def seed(self):
        return self._data['seed']

    @property
    def weights(self):
        return dict(self._data['weights'])

    @property
    def emergence_threshold(self):
        return self._data['emergence_threshold']

    @property
    def max_rounds(self):
        return self._data['max_rounds']

    def get_param(self, module: str, key: str, default=None):
        """Get a paper_param value: config.get_param('calculator', 'W_K') → 0.35"""
        return self._data.get('paper_params', {}).get(module, {}).get(key, default)

    def to_dict(self):
        return copy.deepcopy(self._data)

    def __repr__(self):
        return f"QCMConfig(mode={self.mode}, plugins={self.active_plugins})"


def load_config(source=None):
    if source is None:
        return QCMConfig()
    if isinstance(source, dict):
        return QCMConfig.from_dict(source)
    if isinstance(source, str):
        if source.endswith('.json'):
            return QCMConfig.from_json(source)
        if source.endswith(('.yaml', '.yml')):
            return QCMConfig.from_yaml(source)
    raise ValueError(f"Unsupported config source: {type(source)}")
