# 🦊 FoxRead API - 狡黠的内容猎手

> "像狐狸一样聪明地获取网页内容"

一个智能的网页内容提取API服务，专注于突破反爬虫限制，获取高质量的网页内容。

## ✨ 特性

- 🧠 **智能绕过** - 突破反爬虫限制
- ⚡ **敏捷提取** - 快速获取核心内容  
- 🎨 **多格式输出** - 支持JSON/Text/Markdown
- 🔥 **知乎专栏** - 100%成功率
- 🌐 **广泛兼容** - 支持各种复杂网站

## 🚀 快速开始

### 1. 环境安装

```bash
# 运行自动安装脚本
python3 install.py
```

安装脚本会自动：
- 检查Python版本（需要 ≥ 3.8）
- 安装所需依赖包
- 配置Chrome浏览器和驱动
- 创建启动脚本

### 2. 启动服务

```bash
# Linux/macOS
./start.sh

# Windows
start.bat

# 或直接运行
python3 foxread_api.py
```

服务启动后访问：http://localhost:8900

## 📖 API 使用

### 基本用法

```bash
# 获取服务信息
curl http://localhost:8900/

# 健康检查
curl http://localhost:8900/health

# 能力测试
curl http://localhost:8900/test
```

### 内容提取

```bash
# 方式1: 查询参数
curl "http://localhost:8900/api?url=https://zhuanlan.zhihu.com/p/579628061&format=json"

# 方式2: 路径参数 (推荐)
curl "http://localhost:8900/extract/https://zhuanlan.zhihu.com/p/579628061?format=markdown"
```

### 输出格式

- `json` - 完整的JSON响应（默认）
- `text` - 纯文本内容
- `markdown` - Markdown格式

## 🛠️ 技术架构

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   Web Agent      │    │   Chrome        │
│   异步API服务    │───▶│   智能爬虫引擎    │───▶│   无头浏览器     │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 核心组件

- **FastAPI**: 高性能异步Web框架
- **Selenium**: 浏览器自动化驱动
- **BeautifulSoup**: HTML内容解析
- **Chrome**: 无头浏览器引擎

### 反爬虫策略

1. **智能识别**: 自动识别网站类型，采用对应策略
2. **请求伪装**: 模拟真实浏览器行为
3. **动态等待**: 智能等待页面加载完成
4. **JavaScript反检测**: 隐藏自动化特征

## 🎯 支持的网站

### 高难度站点 (🔥 专项优化)
- 知乎专栏 - 100%成功率
- 微博内容
- CSDN博客
- 简书文章

### 通用站点 (⚡ 快速处理)
- 新闻网站
- 博客文章
- 技术文档
- 普通网页

## 📊 API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 服务首页和信息 |
| `/health` | GET | 健康检查 |
| `/api` | GET | 标准API接口 |
| `/extract/{url:path}` | GET | RESTful风格接口 |
| `/test` | GET | 能力测试 |
| `/docs` | GET | API文档 (Swagger) |

## 🔧 配置说明

### 环境变量
```bash
export FOXREAD_PORT=8900
export FOXREAD_HOST=0.0.0.0
export FOXREAD_TIMEOUT=30
```

### Chrome选项
可以通过修改 `web_agent.py` 中的 `chrome_options` 来调整浏览器配置。

## 🐛 故障排除

### 常见问题

1. **Chrome未安装**
   ```bash
   # macOS
   brew install --cask google-chrome
   
   # Ubuntu
   sudo apt install google-chrome-stable
   ```

2. **依赖安装失败**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **权限问题**
   ```bash
   chmod +x start.sh
   chmod +x install.py
   ```

### 调试模式

```bash
# 查看详细日志
python3 foxread_api.py --debug

# 测试web_agent
python3 web_agent.py "https://example.com" --pretty
```

## 📈 性能优化

- 使用SSD存储提升启动速度
- 增加内存避免Chrome崩溃
- 部署到云服务器提升网络速度
- 配置反向代理提升并发能力

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本项目
2. 创建特性分支
3. 提交改动
4. 发起Pull Request

## 📜 开源协议

本项目采用 MIT 协议开源。

## 🦊 Fox Wisdom

> "在信息的森林里，做最聪明的猎手"

---

**FoxRead API** - 让内容获取变得简单而智能 🚀
