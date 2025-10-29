#!/usr/bin/env python3
"""
Web Agent 改进版 - 基于测试结果优化
集成了v1版本的成功配置
"""

import sys
import subprocess
import argparse
import json
import time
from urllib.parse import urlparse

def check_dependencies():
    """检查依赖"""
    try:
        import selenium, bs4
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "beautifulsoup4", "webdriver-manager"])

check_dependencies()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def is_social_media(url):
    """检测社交媒体网站"""
    domains = ['twitter.com', 'x.com', 'facebook.com', 'instagram.com']
    return any(d in urlparse(url).netloc.lower() for d in domains)

def is_complex_site(url):
    """检测复杂网站(需要完整反检测的网站)"""
    domains = ['zhihu.com', 'weibo.com', 'csdn.net', 'jianshu.com']
    return any(d in urlparse(url).netloc.lower() for d in domains)

def get_content(url):
    """获取页面内容 - 改进版配置"""
    chrome_options = Options()
    
    # 基础配置
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    # 🔑 User-Agent (必需)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # 根据网站类型配置
    stealth = is_social_media(url) or is_complex_site(url)
    
    if stealth:
        # 完整反检测配置 (对知乎等复杂网站必需)
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    else:
        # 普通网站优化
        chrome_options.add_argument('--disable-images')
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        if stealth:
            # JavaScript反检测 (关键!)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # HTTP Headers设置
            custom_headers = {
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {'headers': custom_headers})
        
        driver.get(url)
        
        if stealth:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(3)
        else:
            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        
        content = driver.page_source
        title = driver.title
        
        return content, title
        
    except Exception as e:
        print(f"访问失败: {e}")
        return None, ""
    finally:
        try:
            driver.quit()
        except:
            pass

def extract_content(html, url, title):
    """提取内容"""
    if not html:
        return {"title": "", "url": url, "content": "访问失败"}
    
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator='\n', strip=True)
    
    return {
        "title": title or (soup.find('title').get_text().strip() if soup.find('title') else ""),
        "url": url,
        "content": text,
        "content_type": "text/html"
    }

def main():
    parser = argparse.ArgumentParser(description='Web Agent 改进版')
    parser.add_argument('url')
    parser.add_argument('-o', '--output')
    parser.add_argument('--pretty', action='store_true')
    args = parser.parse_args()
    
    html, title = get_content(args.url)
    result = extract_content(html, args.url, title)
    
    output = json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
    else:
        print(output)

if __name__ == "__main__":
    main()
