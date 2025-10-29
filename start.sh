#!/bin/bash
# 🦊 FoxRead API 启动脚本

cd "/Users/cloudv/Desktop/FoxRead API"

echo "🦊============================================================🦊"
echo "🦊 FoxRead API - 狡黠的内容猎手"
echo "🦊 \"像狐狸一样聪明地获取网页内容\""
echo "🦊============================================================🦊"

# 检查Python依赖
echo "🔍 检查依赖..."
/Users/cloudv/miniconda3/bin/python3 -c "import fastapi, uvicorn, selenium, bs4, webdriver_manager; print('✅ 所有依赖正常')" || {
    echo "❌ 依赖检查失败，请运行: python3 install.py"
    exit 1
}

# 启动服务
echo "🚀 启动FoxRead API..."
/Users/cloudv/miniconda3/bin/python3 foxread_api.py
