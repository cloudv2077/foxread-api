@echo off
cd /d "/Users/cloudv/Desktop/FoxRead API"

echo 🦊============================================================🦊
echo 🦊 FoxRead API - 狡黠的内容猎手
echo 🦊 "像狐狸一样聪明地获取网页内容"
echo 🦊============================================================🦊

echo 🔍 检查依赖...
/Users/cloudv/miniconda3/bin/python3 -c "import fastapi, uvicorn, selenium, bs4, webdriver_manager; print('✅ 所有依赖正常')" || (
    echo ❌ 依赖检查失败，请运行: python install.py
    pause
    exit /b 1
)

echo 🚀 启动FoxRead API...
/Users/cloudv/miniconda3/bin/python3 foxread_api.py
pause
