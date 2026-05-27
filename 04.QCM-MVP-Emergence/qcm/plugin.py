"""QCM Plugin Registry — 插件註冊與管理"""
import importlib


class PluginSpec:
    def __init__(self, name, module_path, class_name, layer, formulas, enabled=True):
        self.name = name
        self.module_path = module_path
        self.class_name = class_name
        self.layer = layer
        self.formulas = formulas
        self.enabled = enabled
        self._instance = None

    def instantiate(self, **kwargs):
        mod = importlib.import_module(self.module_path)
        cls = getattr(mod, self.class_name)
        self._instance = cls(**kwargs)
        return self._instance

    @property
    def instance(self):
        return self._instance

    def __repr__(self):
        return f"Plugin({self.name}, L{self.layer}, {self.formulas})"


class PluginRegistry:
    def __init__(self):
        self._plugins = {}
        self._execution_order = []

    def register(self, spec):
        self._plugins[spec.name] = spec
        if spec.name not in self._execution_order:
            self._execution_order.append(spec.name)

    def get(self, name):
        return self._plugins.get(name)

    @property
    def all(self):
        return dict(self._plugins)

    @property
    def active(self):
        return {n: p for n, p in self._plugins.items() if p.enabled}

    def enable(self, name):
        if name in self._plugins:
            self._plugins[name].enabled = True

    def disable(self, name):
        if name in self._plugins:
            self._plugins[name].enabled = False

    def enable_by_config(self, config):
        for name, spec in self._plugins.items():
            spec.enabled = config.get(f'plugins.{name}', True)

    def by_layer(self, layer):
        return [p for p in self._plugins.values() if p.layer == layer and p.enabled]

    def execution_list(self):
        return [self._plugins[n] for n in self._execution_order if n in self._plugins and self._plugins[n].enabled]

    def __repr__(self):
        total = len(self._plugins)
        active = len(self.active)
        return f"PluginRegistry({active}/{total} active)"


plugin_registry = PluginRegistry()

plugin_registry.register(PluginSpec("epr", "epr_entanglement", "EPREntanglement", 2, "F6"))
plugin_registry.register(PluginSpec("dw", "dynamic_weight", "DynamicWeightCalculator", 2, "F7"))
plugin_registry.register(PluginSpec("mdist", "mahalanobis_distance", "ContrastiveLoss", 3, "F8-F9"))
plugin_registry.register(PluginSpec("rcs", "rcs_hybrid", "RCSHybrid", 3, "F10-F11"))
plugin_registry.register(PluginSpec("deadlock", "deadlock_detector", "DeadlockDetector", 3, "F12-F13"))
plugin_registry.register(PluginSpec("sandbox", "sandbox", "SandboxManager", 4, "F14-F15"))
plugin_registry.register(PluginSpec("flywheel", "flywheel", "FlywheelOptimizer", 4, "F16-F18"))
plugin_registry.register(PluginSpec("kgrowth", "knowledge_growth", "KnowledgeGrowthEngine", 4, "F19-F20"))
plugin_registry.register(PluginSpec("router", "neural_router", "NeuralRouter", 5, "F21"))
plugin_registry.register(PluginSpec("pareto", "pareto_cost", "ParetoCostCalculator", 5, "F22"))
