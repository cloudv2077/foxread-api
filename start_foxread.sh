#!/bin/bash

# 🦊 FoxRead API 启动脚本
# "像狐狸一样聪明地获取网页内容"

echo "🦊========================================🦊"
echo "🦊 FoxRead API - 狡黠的内容猎手"
echo "🦊 \"像狐狸一样聪明地获取网页内容\""
echo "🦊========================================🦊"

# 检查必要文件
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FOXREAD_API="$SCRIPT_DIR/foxread_api.py"
WEB_AGENT="$HOME/Linkgo/web_agent.py"

if [ ! -f "$FOXREAD_API" ]; then
    echo "❌ FoxRead API文件不存在: $FOXREAD_API"
    exit 1
fi

if [ ! -f "$WEB_AGENT" ]; then
    echo "⚠️  Web Agent不存在: $WEB_AGENT"
    echo "🦊 狐狸缺少狩猎工具，但仍会尝试启动..."
fi

# 停止现有服务
echo "🔄 停止现有FoxRead服务..."
pkill -f "foxread_api.py" 2>/dev/null || true
pkill -f "webagent_api" 2>/dev/null || true
sleep 2

# 启动FoxRead服务
echo "🚀 启动FoxRead API服务..."
cd "$SCRIPT_DIR"

# 后台运行
nohup python foxread_api.py > foxread.log 2>&1 &
FOXREAD_PID=$!

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 3

# 检查服务状态
if ps -p $FOXREAD_PID > /dev/null 2>&1; then
    echo "✅ FoxRead服务启动成功! PID: $FOXREAD_PID"
    echo ""
    echo "🎯 服务地址:"
    echo "   📍 主页: http://localhost:8900"
    echo "   📚 文档: http://localhost:8900/docs"  
    echo "   🧪 测试: http://localhost:8900/test"
    echo "   💚 健康: http://localhost:8900/health"
    echo ""
    echo "🦊 使用示例:"
    echo "   curl \"http://localhost:8900/api?url=https://zhuanlan.zhihu.com/p/579628061\""
    echo "   curl \"http://localhost:8900/extract/zhuanlan.zhihu.com/p/579628061\""
    echo ""
    echo "🦊 FoxRead正在森林中等待您的狩猎指令! 🏹"
else
    echo "❌ FoxRead服务启动失败!"
    echo "📝 查看日志: cat $SCRIPT_DIR/foxread.log"
    exit 1
fi

echo "🦊========================================🦊"
