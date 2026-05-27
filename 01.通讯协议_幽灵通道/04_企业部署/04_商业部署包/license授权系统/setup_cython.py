# Ghost Channel Enterprise - Cython Build Configuration

from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension(
        "ghost_channel_enterprise.semantics",
        ["ghost_channel_enterprise/semantics.pyx"],
        extra_compile_args=["/O2"],
    ),
    Extension(
        "ghost_channel_enterprise.predictive",
        ["ghost_channel_enterprise/predictive.pyx"],
        extra_compile_args=["/O2"],
    ),
    Extension(
        "ghost_channel_enterprise.knowledge_graph",
        ["ghost_channel_enterprise/knowledge_graph.pyx"],
        extra_compile_args=["/O2"],
    ),
]

setup(
    name="ghost-channel-enterprise",
    version="1.0.0",
    packages=[],
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": "3",
            "embedsignature": True,
            "binding": True,
        },
    ),
)
