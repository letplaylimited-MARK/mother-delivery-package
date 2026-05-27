# -*- coding: utf-8 -*-
"""
Ghost Hub API 启动脚本
"""

import sys
import os

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    from ghost_hub_sdk.api.main import app

    print("=" * 50)
    print("Ghost Hub API 服务器")
    print("=" * 50)
    print("Swagger UI: http://localhost:8080/docs")
    print("ReDoc: http://localhost:8080/redoc")
    print("=" * 50)

    uvicorn.run(app, host="0.0.0.0", port=8080)
