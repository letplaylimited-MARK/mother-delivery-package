"""
Ghost Channel Enterprise - Cython Build Setup
幽灵通道商业版 - Cython编译配置

使用说明:
---------

Linux/Mac:
    pip install cython numpy
    python setup.py build_ext --inplace

Windows (需要Visual Studio):
    1. 安装 Visual Studio Build Tools
    2. pip install cython numpy
    3. python setup.py build_ext --inplace

或者使用预编译版本:
    pip install ghost-channel-enterprise预编译版将提供预编译的.pyd文件
"""

import os
import sys
from setuptools import setup, Extension
from Cython.Build import cythonize

# 模块列表
modules = [
    "semantics",
    "predictive",
    "knowledge_graph",
]

extensions = []
for module in modules:
    pyx_file = f"ghost_channel_enterprise/{module}.pyx"
    if os.path.exists(pyx_file):
        extensions.append(
            Extension(
                f"ghost_channel_enterprise.{module}",
                [pyx_file],
                extra_compile_args=["/O2"]
                if sys.platform == "win32"
                else ["-O3", "-march=native"],
            )
        )


def build():
    """构建并安装"""
    setup(
        name="ghost-channel-enterprise",
        version="1.0.0",
        packages=["ghost_channel_enterprise"],
        ext_modules=cythonize(
            extensions,
            compiler_directives={
                "language_level": "3",
                "embedsignature": True,
                "boundscheck": False,
                "wraparound": False,
            },
        ),
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build_ext":
        build()
    else:
        print("Usage: python setup.py build_ext --inplace")
        print("")
        print("This will compile .pyx files to .pyd (Windows) or .so (Linux/Mac)")
        print("")
        print("Requirements:")
        print("  - Cython >= 3.0")
        print("  - On Windows: Visual Studio Build Tools")
        print("  - On Linux/Mac: gcc/clang")
