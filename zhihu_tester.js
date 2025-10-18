#!/usr/bin/env node

const https = require('https');
const http = require('http');
const zlib = require('zlib');
const { URL } = require('url');

// Google搜索获取知乎URL
function searchZhihuUrls(query) {
    return new Promise((resolve) => {
        const searchUrl = `https://www.google.com/search?q=site:zhihu.com+${encodeURIComponent(query)}`;
        console.log(`🔍 Google搜索: ${query}`);
        console.log(`📍 搜索URL: ${searchUrl}`);
        
        const options = {
            hostname: 'www.google.com',
            path: `/search?q=site:zhihu.com+${encodeURIComponent(query)}`,
            method: 'GET',
            headers: {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            },
            timeout: 10000
        };

        const req = https.request(options, (res) => {
            let stream = res;
            if (res.headers['content-encoding'] === 'gzip') {
                stream = res.pipe(zlib.createGunzip());
            } else if (res.headers['content-encoding'] === 'deflate') {
                stream = res.pipe(zlib.createInflate());
            }
            
            let data = '';
            stream.on('data', chunk => data += chunk);
            stream.on('end', () => {
                // 提取知乎链接
                const zhihuUrls = [];
                const urlPattern = /https?:\/\/[^"'\s]*zhihu\.com[^"'\s]*/g;
                let matches = data.match(urlPattern) || [];
                
                // 清理和去重
                const cleanUrls = [...new Set(matches)]
                    .filter(url => !url.includes('google.com'))
                    .filter(url => !url.includes('cache:'))
                    .slice(0, 5); // 取前5个

                console.log(`✅ 找到 ${cleanUrls.length} 个知乎链接`);
                resolve(cleanUrls);
            });
        });

        req.on('error', (error) => {
            console.log(`❌ Google搜索失败: ${error.message}`);
            // 返回一些备用的知乎URL
            const backupUrls = [
                'https://zhuanlan.zhihu.com/p/579628061',
                'https://www.zhihu.com/question/20297063',
                'https://zhuanlan.zhihu.com/p/400000000',
                'https://www.zhihu.com/question/300000000'
            ];
            console.log(`🔄 使用备用URL列表`);
            resolve(backupUrls);
        });

        req.on('timeout', () => {
            console.log('⏱️ Google搜索超时');
            req.destroy();
            resolve([]);
        });

        req.end();
    });
}

// 测试单个URL
function testZhihuUrl(url) {
    return new Promise((resolve) => {
        console.log(`\n🔍 测试: ${url}`);
        console.log('-'.repeat(60));
        
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
                timeout: 15000
            };

            const startTime = Date.now();
            
            const req = https.request(options, (res) => {
                const responseTime = Date.now() - startTime;
                
                console.log(`⏱️  响应时间: ${responseTime}ms`);
                console.log(`📊 状态码: ${res.statusCode}`);
                console.log(`🏷️  服务器: ${res.headers.server || 'Unknown'}`);
                
                if (res.headers.location) {
                    console.log(`🔀 重定向: ${res.headers.location}`);
                }
                
                let stream = res;
                if (res.headers['content-encoding'] === 'gzip') {
                    stream = res.pipe(zlib.createGunzip());
                } else if (res.headers['content-encoding'] === 'deflate') {
                    stream = res.pipe(zlib.createInflate());
                } else if (res.headers['content-encoding'] === 'br') {
                    stream = res.pipe(zlib.createBrotliDecompress());
                }
                
                let data = '';
                stream.on('data', chunk => data += chunk);
                stream.on('end', () => {
                    console.log(`📄 内容长度: ${data.length} 字符`);
                    
                    // 分析结果
                    let status, analysis;
                    if (res.statusCode === 200) {
                        if (data.length > 5000) {
                            status = '✅ 成功访问';
                            analysis = '获取到完整页面内容';
                        } else {
                            status = '⚠️ 部分成功';
                            analysis = '内容较少，可能是简化版';
                        }
                    } else if (res.statusCode === 403) {
                        status = '🛡️ 反爬虫拦截';
                        analysis = '触发知乎反爬虫机制';
                    } else if (res.statusCode >= 300 && res.statusCode < 400) {
                        status = '🔀 重定向';
                        analysis = '页面重定向';
                    } else {
                        status = '❌ 访问失败';
                        analysis = `HTTP ${res.statusCode}`;
                    }
                    
                    console.log(`🎯 结果: ${status}`);
                    console.log(`💡 分析: ${analysis}`);
                    
                    // 提取标题
                    const titleMatch = data.match(/<title>(.*?)<\/title>/i);
                    if (titleMatch && titleMatch[1].trim()) {
                        const title = titleMatch[1].trim();
                        console.log(`📰 标题: ${title.length > 60 ? title.substring(0, 60) + '...' : title}`);
                    }
                    
                    // 内容预览
                    if (data.length > 100) {
                        const preview = data.replace(/\s+/g, ' ').trim().substring(0, 150);
                        console.log(`👀 预览: ${preview}...`);
                    }
                    
                    resolve({
                        url,
                        statusCode: res.statusCode,
                        contentLength: data.length,
                        responseTime,
                        status,
                        analysis
                    });
                });
                
                stream.on('error', (error) => {
                    console.log(`❌ 内容处理失败: ${error.message}`);
                    resolve({ url, error: error.message, status: 'failed' });
                });
            });

            req.on('error', (error) => {
                console.log(`❌ 请求失败: ${error.message}`);
                resolve({ url, error: error.message, status: 'failed' });
            });

            req.on('timeout', () => {
                console.log('❌ 请求超时');
                req.destroy();
                resolve({ url, error: '超时', status: 'timeout' });
            });

            req.end();
            
        } catch (error) {
            console.log(`❌ URL错误: ${error.message}`);
            resolve({ url, error: error.message, status: 'failed' });
        }
    });
}

async function main() {
    console.log('🚀 知乎访问测试工具 v2.0');
    console.log('='.repeat(50));
    console.log(`📅 测试时间: ${new Date().toLocaleString()}`);
    
    const args = process.argv.slice(2);
    
    let urlsToTest = [];
    
    if (args.length === 0) {
        // 默认搜索一些热门关键词
        console.log('\n🔍 未提供参数，使用默认搜索...');
        const queries = ['人工智能', 'Python编程', 'React开发'];
        
        for (const query of queries) {
            console.log(`\n📋 搜索关键词: ${query}`);
            const urls = await searchZhihuUrls(query);
            urlsToTest.push(...urls);
            
            // 搜索间隔
            if (queries.indexOf(query) < queries.length - 1) {
                console.log('⏳ 等待2秒...');
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
        }
    } else if (args[0].startsWith('http')) {
        // 直接测试提供的URL
        urlsToTest = [args[0]];
    } else {
        // 搜索指定关键词
        console.log(`\n🔍 搜索关键词: ${args.join(' ')}`);
        urlsToTest = await searchZhihuUrls(args.join(' '));
    }
    
    // 去重
    urlsToTest = [...new Set(urlsToTest)].slice(0, 5);
    
    if (urlsToTest.length === 0) {
        console.log('❌ 没有找到可测试的URL');
        return;
    }
    
    console.log(`\n📝 将测试 ${urlsToTest.length} 个URL:`);
    urlsToTest.forEach((url, index) => {
        console.log(`${index + 1}. ${url}`);
    });
    
    // 执行测试
    console.log('\n🧪 开始测试...');
    const results = [];
    
    for (let i = 0; i < urlsToTest.length; i++) {
        console.log(`\n[${i + 1}/${urlsToTest.length}]`);
        const result = await testZhihuUrl(urlsToTest[i]);
        results.push(result);
        
        // 测试间隔
        if (i < urlsToTest.length - 1) {
            console.log('⏳ 等待2秒后继续...');
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
    }
    
    // 生成报告
    console.log('\n' + '='.repeat(60));
    console.log('📊 测试结果汇总');
    console.log('='.repeat(60));
    
    let successCount = 0;
    let blockedCount = 0;
    let failedCount = 0;
    
    results.forEach((result, index) => {
        console.log(`\n${index + 1}. ${result.url}`);
        console.log(`   状态: ${result.status}`);
        if (result.analysis) console.log(`   分析: ${result.analysis}`);
        if (result.statusCode) console.log(`   状态码: ${result.statusCode}`);
        if (result.responseTime) console.log(`   响应时间: ${result.responseTime}ms`);
        
        if (result.status && result.status.includes('成功')) {
            successCount++;
        } else if (result.status && result.status.includes('反爬虫')) {
            blockedCount++;
        } else {
            failedCount++;
        }
    });
    
    console.log('\n📈 统计:');
    console.log(`✅ 成功: ${successCount} 个`);
    console.log(`🛡️ 被拦截: ${blockedCount} 个`);
    console.log(`❌ 失败: ${failedCount} 个`);
    
    const successRate = ((successCount / results.length) * 100).toFixed(1);
    console.log(`🎯 成功率: ${successRate}%`);
    
    console.log('\n🏁 测试完成!');
}

// 使用说明
if (process.argv.length === 2 || (process.argv.length === 3 && process.argv[2] === '--help')) {
    console.log('🚀 知乎访问测试工具');
    console.log('\n使用方法:');
    console.log('  node zhihu_tester.js                    # 默认搜索测试');
    console.log('  node zhihu_tester.js <关键词>            # 搜索指定关键词');
    console.log('  node zhihu_tester.js <URL>              # 测试指定URL');
    console.log('\n示例:');
    console.log('  node zhihu_tester.js');
    console.log('  node zhihu_tester.js "机器学习"');
    console.log('  node zhihu_tester.js "JavaScript 教程"');
    console.log('  node zhihu_tester.js https://zhuanlan.zhihu.com/p/123456');
    process.exit(0);
}

main().catch(console.error);
