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
