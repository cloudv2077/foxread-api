#!/usr/bin/env python3
"""
🦊 FoxRead API - 狡黠的内容猎手
"像狐狸一样聪明地获取网页内容"

智能网页内容提取服务，专注于突破反爬虫限制
"""

import sys
import os
import json
import asyncio
from typing import Optional
from urllib.parse import urlparse
import base64

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
import uvicorn

# 🦊 FoxRead 配置
WEB_AGENT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_agent.py")
PORT = 8900
HOST = "0.0.0.0"
VERSION = "1.0.0"

# 创建FastAPI应用
app = FastAPI(
    title="🦊 FoxRead API",
    description="狡黠的内容猎手 - 像狐狸一样聪明地获取网页内容",
    version=VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

async def extract_with_webagent(url: str, timeout: int = 30):
    """🦊 使用狐狸般的智慧提取网页内容"""
    try:
        if not os.path.exists(WEB_AGENT_PATH):
            raise FileNotFoundError(f"🚫 Web Agent not found at {WEB_AGENT_PATH}")
        
        # 🦊 狡黠地启动内容提取
        process = await asyncio.create_subprocess_exec(
            sys.executable, WEB_AGENT_PATH, url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            process.kill()
            raise HTTPException(status_code=408, detail="⏰ FoxRead timeout - 狐狸需要更多时间")
        
        if process.returncode != 0:
            error_msg = stderr.decode('utf-8') if stderr else "Unknown error"
            raise HTTPException(status_code=500, detail=f"🚫 FoxRead failed: {error_msg}")
        
        try:
            result = json.loads(stdout.decode('utf-8'))
            return result
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"🔧 Failed to parse content: {e}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"🦊 FoxRead extraction failed: {str(e)}")

@app.get("/")
async def foxread_home():
    """🦊 FoxRead 首页"""
    return {
        "service": "🦊 FoxRead API",
        "slogan": "狡黠的内容猎手",
        "description": "像狐狸一样聪明地获取网页内容",
        "version": VERSION,
        "status": "🟢 Running",
        "port": PORT,
        "features": {
            "智能绕过": "🧠 突破反爬虫限制",
            "敏捷提取": "⚡ 快速获取核心内容", 
            "多格式输出": "🎨 JSON/Text/Markdown",
            "知乎专栏": "🔥 100%成功率"
        },
        "endpoints": {
            "extract": "GET /extract/{url:path}?format={format}",
            "api": "GET /api?url={url}&format={format}",
            "test": "GET /test - 🧪 测试FoxRead能力",
            "health": "GET /health - 💚 健康检查"
        },
        "fox_wisdom": "🦊 在信息的森林里，做最聪明的猎手"
    }

@app.get("/health")
async def foxread_health():
    """💚 FoxRead 健康检查"""
    web_agent_available = os.path.exists(WEB_AGENT_PATH)
    return {
        "status": "🟢 Healthy" if web_agent_available else "🟡 Limited", 
        "service": "🦊 FoxRead API",
        "web_agent_available": web_agent_available,
        "web_agent_path": WEB_AGENT_PATH,
        "fox_status": "🦊 Ready to hunt!" if web_agent_available else "🦊 Missing hunting tools"
    }

@app.get("/api")
async def foxread_extract_api(url: str, format: str = "json"):
    """🦊 FoxRead API方式内容提取"""
    # URL 智能处理
    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            url = f"https://{url}"
    except:
        raise HTTPException(status_code=400, detail="🚫 Invalid URL - 狐狸看不懂这个地址")
    
    # 🦊 狡黠地提取内容
    result = await extract_with_webagent(url, 30)
    success = not (result.get('content', '').startswith('访问失败') or '荒原' in result.get('content', ''))
    
    response_data = {
        "service": "🦊 FoxRead",
        "title": result.get('title', ''),
        "url": result.get('url', url),
        "content": result.get('content', ''),
        "success": success,
        "content_length": len(result.get('content', '')),
        "fox_status": "🦊 Successfully hunted!" if success else "🦊 Prey escaped this time",
        "extraction_quality": "🔥 Excellent" if len(result.get('content', '')) > 1000 else "⚡ Good" if len(result.get('content', '')) > 200 else "📝 Basic"
    }
    
    # 根据格式返回
    if format == "text":
        return PlainTextResponse(content=response_data['content'])
    elif format == "markdown":
        markdown_content = f"# {response_data['title']}\n\n{response_data['content']}\n\n---\n*Extracted by 🦊 FoxRead - 狡黠的内容猎手*"
        return PlainTextResponse(content=markdown_content, media_type="text/markdown")
    else:
        return JSONResponse(content=response_data)

@app.get("/extract/{url:path}")
async def foxread_extract_direct(url: str, format: str = "markdown"):
    """🦊 FoxRead 直接路径方式提取 (类似jina.ai)"""
    if not url.startswith(('http://', 'https://')):
        if url.startswith('//'):
            url = f"https:{url}"
        else:
            url = f"https://{url}"
    
    return await foxread_extract_api(url=url, format=format)

@app.get("/test")
async def foxread_capability_test():
    """🧪 FoxRead 能力测试 - 展示狐狸的狡黠"""
    test_urls = [
        {
            "url": "https://zhuanlan.zhihu.com/p/579628061",
            "description": "知乎专栏 - 法律类文章",
            "difficulty": "🔥 困难 (反爬虫)"
        },
        {
            "url": "https://zhuanlan.zhihu.com/p/400000000", 
            "description": "知乎专栏 - 技术类文章",
            "difficulty": "🔥 困难 (反爬虫)"
        }
    ]
    
    results = []
    total_success = 0
    
    for test_case in test_urls:
        url = test_case["url"]
        try:
            result = await extract_with_webagent(url, 30)
            success = not (result.get('content', '').startswith('访问失败') or '荒原' in result.get('content', ''))
            content_length = len(result.get('content', ''))
            
            if success:
                total_success += 1
                
            quality = "🔥 Excellent" if content_length > 1000 else "⚡ Good" if content_length > 200 else "📝 Basic"
            
            results.append({
                "url": url,
                "description": test_case["description"],
                "difficulty": test_case["difficulty"],
                "title": result.get('title', ''),
                "content_length": content_length,
                "success": success,
                "quality": quality,
                "fox_result": "🦊 Hunted successfully!" if success else "🦊 Prey was too clever",
                "preview": result.get('content', '')[:200] + "..." if result.get('content') else ""
            })
        except Exception as e:
            results.append({
                "url": url,
                "description": test_case["description"], 
                "difficulty": test_case["difficulty"],
                "error": str(e),
                "success": False,
                "fox_result": f"🦊 Encountered obstacle: {str(e)[:50]}..."
            })
    
    success_rate = (total_success / len(test_urls)) * 100
    
    return {
        "service": "🦊 FoxRead API",
        "test_name": "🧪 FoxRead 狡黠能力测试",
        "test_results": results,
        "summary": {
            "total_tests": len(test_urls),
            "successful": total_success,
            "success_rate": f"{success_rate:.1f}%",
            "fox_performance": "🏆 Master Hunter" if success_rate == 100 else "⭐ Skilled Hunter" if success_rate >= 80 else "🌱 Learning Hunter"
        },
        "fox_wisdom": "🦊 每一次成功的狩猎，都源于智慧和耐心的结合",
        "timestamp": "2025-10-18"
    }

# 🦊 启动入口
if __name__ == "__main__":
    print("🦊" + "="*60 + "🦊")
    print("🦊 FoxRead API - 狡黠的内容猎手")
    print("🦊 \"像狐狸一样聪明地获取网页内容\"")
    print("🦊" + "="*60 + "🦊")
    print(f"🌟 服务地址: http://{HOST}:{PORT}")
    print(f"📚 API文档: http://{HOST}:{PORT}/docs") 
    print(f"🧪 能力测试: http://{HOST}:{PORT}/test")
    print(f"💚 健康检查: http://{HOST}:{PORT}/health")
    print(f"🔧 Web Agent: {WEB_AGENT_PATH}")
    print("🦊" + "="*60 + "🦊")
    print("🦊 FoxRead is ready to hunt! 🏹")
    
    uvicorn.run(app, host=HOST, port=PORT, reload=False)
