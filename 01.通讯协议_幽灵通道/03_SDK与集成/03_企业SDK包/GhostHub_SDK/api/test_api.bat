@echo off
chcp 65001 >nul
echo ==================== API 测试 ====================

echo.
echo [1] 健康检查
curl -s http://localhost:8080/health
echo.

echo.
echo [2] 模板列表
curl -s http://localhost:8080/api/v1/templates
echo.

echo.
echo [3] 设备列表
curl -s http://localhost:8080/api/v1/devices
echo.

echo.
echo [4] 智能体列表
curl -s http://localhost:8080/api/v1/agents
echo.

echo.
echo [5] 意图匹配
curl -s -X POST http://localhost:8080/api/v1/intent/match -H "Content-Type: application/json" -d "{\"text\":\"打开客厅灯\"}"
echo.

echo.
echo ==================== 测试完成 ====================
pause
