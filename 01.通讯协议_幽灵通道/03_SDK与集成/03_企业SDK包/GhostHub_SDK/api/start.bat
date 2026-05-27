@echo off
chcp 65001 >nul
echo ========================================
echo Ghost Hub API 服务器启动中...
echo ========================================
cd /d "%~dp0\..\.."
python -m ghost_hub_sdk.api.main
