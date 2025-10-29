#!/usr/bin/env python3
"""
🦊 FoxRead API 环境安装脚本
自动安装所需依赖和配置环境
"""

import sys
import os
import subprocess
import platform
import json
from pathlib import Path

class FoxReadInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.required_packages = [
            'fastapi>=0.104.0',
            'uvicorn[standard]>=0.24.0',
            'selenium>=4.15.0',
            'beautifulsoup4>=4.12.0',
            'webdriver-manager>=4.0.0',
            'requests>=2.31.0'
        ]
        self.install_log = []
        
    def log(self, message, success=True):
        """记录安装日志"""
        icon = "✅" if success else "❌"
        print(f"{icon} {message}")
        self.install_log.append({"message": message, "success": success})
    
    def run_command(self, cmd, description=""):
        """执行命令并记录结果"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                self.log(f"{description} - 成功")
                return True, result.stdout
            else:
                self.log(f"{description} - 失败: {result.stderr}", False)
                return False, result.stderr
        except subprocess.TimeoutExpired:
            self.log(f"{description} - 超时", False)
            return False, "Command timeout"
        except Exception as e:
            self.log(f"{description} - 异常: {str(e)}", False)
            return False, str(e)
    
    def check_python_version(self):
        """检查Python版本"""
        self.log("🐍 检查Python版本...")
        if sys.version_info < (3, 8):
            self.log(f"Python版本过低: {self.python_version}, 需要 >= 3.8", False)
            return False
        self.log(f"Python版本: {self.python_version} ✓")
        return True
    
    def install_python_packages(self):
        """安装Python包"""
        self.log("📦 开始安装Python依赖包...")
        
        # 升级pip
        success, output = self.run_command(
            f"{sys.executable} -m pip install --upgrade pip",
            "升级pip"
        )
        
        if not success:
            self.log("pip升级失败，继续安装依赖...", False)
        
        # 安装依赖包
        for package in self.required_packages:
            success, output = self.run_command(
                f"{sys.executable} -m pip install {package}",
                f"安装 {package}"
            )
            if not success:
                self.log(f"安装 {package} 失败", False)
                return False
        
        self.log("所有Python依赖安装完成")
        return True
    
    def install_chrome_driver(self):
        """安装Chrome和ChromeDriver"""
        self.log("🌐 检查Chrome浏览器...")
        
        if self.system == "darwin":  # macOS
            chrome_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium"
            ]
            chrome_found = any(os.path.exists(path) for path in chrome_paths)
            
            if not chrome_found:
                self.log("未找到Chrome浏览器，请手动安装Chrome", False)
                self.log("下载地址: https://www.google.com/chrome/", False)
                return False
            else:
                self.log("Chrome浏览器已安装")
                
        elif self.system == "linux":
            # 检查Chrome是否安装
            success, output = self.run_command("which google-chrome || which chromium-browser", "检查Chrome")
            if not success:
                self.log("正在安装Chrome浏览器...")
                # Ubuntu/Debian
                commands = [
                    "wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -",
                    "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google-chrome.list",
                    "apt-get update",
                    "apt-get install -y google-chrome-stable"
                ]
                for cmd in commands:
                    success, output = self.run_command(f"sudo {cmd}", f"执行: {cmd}")
                    if not success:
                        self.log("Chrome安装失败，请手动安装", False)
                        return False
                self.log("Chrome安装完成")
            else:
                self.log("Chrome浏览器已安装")
        
        # 测试webdriver-manager
        self.log("测试ChromeDriver自动管理...")
        test_code = '''
import sys
sys.path.append(".")
from webdriver_manager.chrome import ChromeDriverManager
driver_path = ChromeDriverManager().install()
print(f"ChromeDriver路径: {driver_path}")
'''
        success, output = self.run_command(f"{sys.executable} -c '{test_code}'", "测试ChromeDriver")
        if success:
            self.log("ChromeDriver自动管理正常")
        else:
            self.log("ChromeDriver配置可能有问题", False)
            
        return True
    
    def test_installation(self):
        """测试安装是否成功"""
        self.log("🧪 测试FoxRead功能...")
        
        # 测试导入
        test_imports = [
            "fastapi",
            "uvicorn", 
            "selenium",
            "bs4",
            "webdriver_manager"
        ]
        
        for module in test_imports:
            try:
                __import__(module)
                self.log(f"导入 {module} 成功")
            except ImportError as e:
                self.log(f"导入 {module} 失败: {e}", False)
                return False
        
        # 测试Selenium基本功能
        test_selenium_code = '''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("data:text/html,<html><body><h1>Test</h1></body></html>")
    title = driver.title
    driver.quit()
    print("Selenium测试成功")
except Exception as e:
    print(f"Selenium测试失败: {e}")
    raise
'''
        
        success, output = self.run_command(f"{sys.executable} -c '{test_selenium_code}'", "测试Selenium")
        if not success:
            self.log("Selenium功能测试失败", False)
            return False
        
        self.log("所有功能测试通过！")
        return True
    
    def create_startup_script(self):
        """创建启动脚本"""
        self.log("📝 创建启动脚本...")
        
        current_dir = Path(__file__).parent
        
        # 创建启动脚本
        startup_script = f'''#!/bin/bash
# 🦊 FoxRead API 启动脚本

cd "{current_dir}"

echo "🦊============================================================🦊"
echo "🦊 FoxRead API - 狡黠的内容猎手"
echo "🦊 \\"像狐狸一样聪明地获取网页内容\\""
echo "🦊============================================================🦊"

# 检查Python依赖
echo "🔍 检查依赖..."
{sys.executable} -c "import fastapi, uvicorn, selenium, bs4, webdriver_manager; print('✅ 所有依赖正常')" || {{
    echo "❌ 依赖检查失败，请运行: python3 install.py"
    exit 1
}}

# 启动服务
echo "🚀 启动FoxRead API..."
{sys.executable} foxread_api.py
'''
        
        with open(current_dir / "start.sh", "w") as f:
            f.write(startup_script)
        
        # 添加执行权限
        os.chmod(current_dir / "start.sh", 0o755)
        self.log("启动脚本创建成功: start.sh")
        
        # Windows批处理文件
        bat_script = f'''@echo off
cd /d "{current_dir}"

echo 🦊============================================================🦊
echo 🦊 FoxRead API - 狡黠的内容猎手
echo 🦊 "像狐狸一样聪明地获取网页内容"
echo 🦊============================================================🦊

echo 🔍 检查依赖...
{sys.executable} -c "import fastapi, uvicorn, selenium, bs4, webdriver_manager; print('✅ 所有依赖正常')" || (
    echo ❌ 依赖检查失败，请运行: python install.py
    pause
    exit /b 1
)

echo 🚀 启动FoxRead API...
{sys.executable} foxread_api.py
pause
'''
        
        with open(current_dir / "start.bat", "w", encoding="utf-8") as f:
            f.write(bat_script)
        
        self.log("Windows启动脚本创建成功: start.bat")
    
    def save_install_report(self):
        """保存安装报告"""
        report = {
            "timestamp": self.get_timestamp(),
            "system": platform.system(),
            "python_version": self.python_version,
            "install_log": self.install_log,
            "success": all(log["success"] for log in self.install_log)
        }
        
        with open("install_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        self.log("安装报告已保存: install_report.json")
    
    def get_timestamp(self):
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def run_installation(self):
        """运行完整安装流程"""
        print("🦊" + "="*60 + "🦊")
        print("🦊 FoxRead API 环境安装器")
        print("🦊 \"让狐狸准备好它的狩猎工具\"")
        print("🦊" + "="*60 + "🦊")
        
        success = True
        
        # 检查Python版本
        if not self.check_python_version():
            success = False
        
        # 安装Python包
        if success and not self.install_python_packages():
            success = False
        
        # 安装Chrome
        if success and not self.install_chrome_driver():
            success = False
        
        # 测试安装
        if success and not self.test_installation():
            success = False
        
        # 创建启动脚本
        if success:
            self.create_startup_script()
        
        # 保存报告
        self.save_install_report()
        
        print("\n🦊" + "="*60 + "🦊")
        if success:
            print("🎉 FoxRead API 安装完成！")
            print("🚀 运行方式:")
            print("   - Linux/Mac: ./start.sh")
            print("   - Windows: start.bat")
            print("   - 直接运行: python3 foxread_api.py")
            print("📚 访问文档: http://localhost:8900/docs")
            print("🧪 测试功能: http://localhost:8900/test")
        else:
            print("❌ 安装过程中遇到问题，请检查install_report.json")
            print("💡 常见解决方案:")
            print("   - 确保Python版本 >= 3.8")
            print("   - 确保网络连接正常")
            print("   - macOS请先安装Chrome浏览器")
            print("   - Linux可能需要sudo权限安装Chrome")
        print("🦊" + "="*60 + "🦊")
        
        return success

if __name__ == "__main__":
    installer = FoxReadInstaller()
    installer.run_installation()
