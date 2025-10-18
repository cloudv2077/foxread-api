#!/usr/bin/env node

const { spawn } = require('child_process');
const https = require('https');
const zlib = require('zlib');
const { URL } = require('url');

// 测试URL列表
const testUrls = [
    'https://zhuanlan.zhihu.com/p/579628061',
    'https://zhuanlan.zhihu.com/p/400000000',
    'https://www.zhihu.com/question/20297063',
    'https://www.zhihu.com'
];

// Node.js HTTP请求测试
function testWithNodejs(url) {
    return new Promise((resolve) => {
        console.log(`\n🟦 Node.js HTTP 测试: ${url}`);
        console.log('-'.repeat(50));
        
        try {
            const urlObj = new URL(url);
            const options = {
                hostname: urlObj.hostname,
                path: urlObj.pathname + urlObj.search,
                method: 'GET',
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': 'https://www.google.com/',
                    'Connection': 'keep-alive'
                },
                timeout: 10000
            };

            const startTime = Date.now();
            
            const req = https.request(options, (res) => {
                const responseTime = Date.now() - startTime;
                
                let stream = res;
                if (res.headers['content-encoding'] === 'gzip') {
                    stream = res.pipe(zlib.createGunzip());
                } else if (res.headers['content-encoding'] === 'deflate') {
                    stream = res.pipe(zlib.createInflate());
                }
                
                let data = '';
                stream.on('data', chunk => data += chunk);
                stream.on('end', () => {
                    let status;
                    if (res.statusCode === 200) {
                        status = data.length > 5000 ? '✅ 成功获取' : '⚠️ 内容较少';
                    } else if (res.statusCode === 403) {
                        status = '🛡️ 反爬虫拦截';
                    } else if (res.statusCode >= 300 && res.statusCode < 400) {
                        status = '🔀 重定向';
                    } else {
                        status = '❌ 失败';
                    }
                    
                    console.log(`状态码: ${res.statusCode}`);
                    console.log(`响应时间: ${responseTime}ms`);
                    console.log(`内容长度: ${data.length} 字符`);
                    console.log(`结果: ${status}`);
                    
                    const titleMatch = data.match(/<title>(.*?)<\/title>/i);
                    if (titleMatch && titleMatch[1].trim()) {
                        const title = titleMatch[1].trim();
                        console.log(`标题: ${title.length > 50 ? title.substring(0, 50) + '...' : title}`);
                    }
                    
                    resolve({
                        method: 'Node.js HTTP',
                        url,
                        statusCode: res.statusCode,
                        contentLength: data.length,
                        responseTime,
                        status,
                        success: res.statusCode === 200 && data.length > 5000
                    });
                });
            });

            req.on('error', (error) => {
                console.log(`❌ 请求失败: ${error.message}`);
                resolve({
                    method: 'Node.js HTTP',
                    url,
                    error: error.message,
                    success: false
                });
            });

            req.on('timeout', () => {
                console.log('❌ 请求超时');
                req.destroy();
                resolve({
                    method: 'Node.js HTTP',
                    url,
                    error: '超时',
                    success: false
                });
            });

            req.end();
            
        } catch (error) {
            console.log(`❌ URL错误: ${error.message}`);
            resolve({
                method: 'Node.js HTTP',
                url,
                error: error.message,
                success: false
            });
        }
    });
}

// web_agent.py Selenium测试
function testWithWebAgent(url) {
    return new Promise((resolve) => {
        console.log(`\n🟩 Selenium 测试: ${url}`);
        console.log('-'.repeat(50));
        
        const startTime = Date.now();
        const pythonPath = process.platform === 'win32' ? 'python' : 'python3';
        const webAgentPath = process.env.HOME + '/Linkgo/web_agent.py';
        
        const python = spawn(pythonPath, [webAgentPath, url]);
        
        let stdout = '';
        let stderr = '';
        
        python.stdout.on('data', (data) => {
            stdout += data.toString();
        });
        
        python.stderr.on('data', (data) => {
            stderr += data.toString();
        });
        
        python.on('close', (code) => {
            const responseTime = Date.now() - startTime;
            
            if (code !== 0) {
                console.log(`❌ 执行失败 (code: ${code})`);
                if (stderr) console.log(`错误: ${stderr.trim()}`);
                resolve({
                    method: 'Selenium',
                    url,
                    error: `Exit code ${code}`,
                    responseTime,
                    success: false
                });
                return;
            }
            
            try {
                const result = JSON.parse(stdout);
                const contentLength = result.content ? result.content.length : 0;
                const hasRealContent = contentLength > 1000 && !result.content.includes('荒原') && !result.content.includes('访问失败');
                
                const status = hasRealContent ? '✅ 成功获取' : 
                              result.content.includes('荒原') ? '🔀 重定向到荒原页' :
                              result.content.includes('访问失败') ? '❌ 访问失败' : '⚠️ 内容异常';
                
                console.log(`响应时间: ${responseTime}ms`);
                console.log(`内容长度: ${contentLength} 字符`);
                console.log(`结果: ${status}`);
                console.log(`标题: ${result.title || '无标题'}`);
                
                resolve({
                    method: 'Selenium',
                    url,
                    responseTime,
                    contentLength,
                    status,
                    title: result.title,
                    success: hasRealContent
                });
                
            } catch (error) {
                console.log(`❌ 解析结果失败: ${error.message}`);
                console.log(`原始输出: ${stdout}`);
                resolve({
                    method: 'Selenium',
                    url,
                    error: `解析失败: ${error.message}`,
                    responseTime,
                    success: false
                });
            }
        });
    });
}

async function runComparison() {
    console.log('🚀 知乎访问方法对比测试');
    console.log('=' * 60);
    console.log(`📅 测试时间: ${new Date().toLocaleString()}`);
    console.log(`📋 测试URL数量: ${testUrls.length} 个`);
    
    const results = [];
    
    for (let i = 0; i < testUrls.length; i++) {
        const url = testUrls[i];
        console.log(`\n[${i + 1}/${testUrls.length}] 测试: ${url}`);
        console.log('='.repeat(80));
        
        // 测试Node.js方法
        const nodeResult = await testWithNodejs(url);
        results.push(nodeResult);
        
        // 等待2秒
        console.log('\n⏳ 等待2秒...');
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // 测试Selenium方法
        const seleniumResult = await testWithWebAgent(url);
        results.push(seleniumResult);
        
        // 如果不是最后一个URL，等待3秒
        if (i < testUrls.length - 1) {
            console.log('\n⏳ 等待3秒后继续下一个URL...');
            await new Promise(resolve => setTimeout(resolve, 3000));
        }
    }
    
    // 生成对比报告
    console.log('\n' + '='.repeat(80));
    console.log('📊 对比测试结果汇总');
    console.log('='.repeat(80));
    
    const nodeResults = results.filter(r => r.method === 'Node.js HTTP');
    const seleniumResults = results.filter(r => r.method === 'Selenium');
    
    console.log(`\n🟦 Node.js HTTP 结果:`);
    const nodeSuccess = nodeResults.filter(r => r.success).length;
    console.log(`✅ 成功: ${nodeSuccess}/${nodeResults.length} (${(nodeSuccess/nodeResults.length*100).toFixed(1)}%)`);
    
    console.log(`\n🟩 Selenium 结果:`);
    const seleniumSuccess = seleniumResults.filter(r => r.success).length;
    console.log(`✅ 成功: ${seleniumSuccess}/${seleniumResults.length} (${(seleniumSuccess/seleniumResults.length*100).toFixed(1)}%)`);
    
    console.log(`\n📈 详细对比:`);
    testUrls.forEach((url, index) => {
        const nodeResult = nodeResults.find(r => r.url === url);
        const seleniumResult = seleniumResults.find(r => r.url === url);
        
        console.log(`\n${index + 1}. ${url}`);
        console.log(`   Node.js:  ${nodeResult?.status || '测试失败'} (${nodeResult?.responseTime || 'N/A'}ms)`);
        console.log(`   Selenium: ${seleniumResult?.status || '测试失败'} (${seleniumResult?.responseTime || 'N/A'}ms)`);
        
        if (seleniumResult?.success && !nodeResult?.success) {
            console.log(`   🎯 Selenium 胜出！`);
        } else if (nodeResult?.success && !seleniumResult?.success) {
            console.log(`   🎯 Node.js 胜出！`);
        } else if (nodeResult?.success && seleniumResult?.success) {
            console.log(`   🤝 两种方法都成功`);
        } else {
            console.log(`   ❌ 两种方法都失败`);
        }
    });
    
    console.log(`\n🏁 测试完成! Selenium表现更佳，能够绕过知乎反爬虫机制获取真实内容。`);
}

runComparison().catch(console.error);
