"""
Ghost Channel Enterprise - 模块入口
幽灵通道商业版 - 模块自动检测与加载

自动检测是否安装了编译版本，如果有则使用，否则回退到源码
"""

import sys
import os

__version__ = "1.0.0"

# 商业功能列表
COMMERCIAL_FEATURES = [
    "semantic_matching",
    "predictive_sync",
    "knowledge_graph",
    "crystallizer",
    "learning_engine",
    "self_healing_pro",
]

# 尝试导入编译版本
_compiled = True
try:
    from ghost_channel_enterprise.semantics import SemanticMatcherPro, SemanticFilterPro
    from ghost_channel_enterprise.predictive import (
        PredictiveSyncPro,
        PredictionResult,
        AdaptiveCompressor,
    )
    from ghost_channel_enterprise.knowledge_graph import (
        KnowledgeGraphPro,
        KnowledgeCrystallizerPro,
    )
except ImportError:
    _compiled = False


# 如果没有编译版本，动态导入源码
if not _compiled:
    import importlib.util

    # 获取源码目录
    _source_dir = os.path.dirname(__file__)

    # 动态加载模块
    def _load_module(name, filename):
        spec = importlib.util.spec_from_file_location(name, filename)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            return module
        return None

    # 加载模块
    _semantics = _load_module(
        "gc_semantics", os.path.join(_source_dir, "semantics.pyx")
    )
    _predictive = _load_module(
        "gc_predictive", os.path.join(_source_dir, "predictive.pyx")
    )
    _knowledge = _load_module(
        "gc_knowledge", os.path.join(_source_dir, "knowledge_graph.pyx")
    )

    if _semantics:
        SemanticMatcherPro = _semantics.SemanticMatcherPro
        SemanticFilterPro = _semantics.SemanticFilterPro

    if _predictive:
        PredictiveSyncPro = _predictive.PredictiveSyncPro
        PredictionResult = _predictive.PredictionResult
        AdaptiveCompressor = _predictive.AdaptiveCompressor

    if _knowledge:
        KnowledgeGraphPro = _knowledge.KnowledgeGraphPro
        KnowledgeCrystallizerPro = _knowledge.KnowledgeCrystallizerPro


def is_compiled() -> bool:
    """检查是否使用编译版本"""
    return _compiled


def get_version() -> str:
    """获取版本"""
    return __version__


def list_features() -> list:
    """列出所有商业功能"""
    return COMMERCIAL_FEATURES.copy()


__all__ = [
    "__version__",
    "is_compiled",
    "get_version",
    "list_features",
    "SemanticMatcherPro",
    "SemanticFilterPro",
    "PredictiveSyncPro",
    "PredictionResult",
    "AdaptiveCompressor",
    "KnowledgeGraphPro",
    "KnowledgeCrystallizerPro",
]
