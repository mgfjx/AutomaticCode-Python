#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cookielib
import urllib2
import urllib
import re
import time
import os
import random
import scrapy

def returnCookies(request):
    # 处理cookie

    if os.path.exists('cookie.txt'):
        # 创建MozillaCookieJar实例对象
        cookie = cookielib.MozillaCookieJar()
        # 从文件中读取cookie内容到变量
        cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
        return cookie
    else:
        # 设置保存cookie的文件，同级目录下的cookie.txt
        filename = 'cookie.txt'
        # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
        cookie = cookielib.MozillaCookieJar(filename)
        # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
        handler = urllib2.HTTPCookieProcessor(cookie)
        # 通过handler来构建opener
        opener = urllib2.build_opener(handler)
        # 创建一个请求，原理同urllib2的urlopen
        response = opener.open(request)
        # 保存cookie到文件
        cookie.save(ignore_discard=True, ignore_expires=True)
        return cookie

def getQsbk(pageSize):
    url = 'http://www.qiushibaike.com/text/' + str(pageSize)
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0)'
    headers = {'User-Agent': user_agent}
    request = urllib2.Request(url)
    request.add_header('User-Agent',user_agent)
    request.add_header('GET',url)
    request.add_header('Host', 'www.qiushibaike.com')
    request.add_header('Referer', url)

    cookie = returnCookies(request)
    # for item in cookie:
    #     print 'Name = ' + item.name
    #     print 'Value = ' + item.value

    # 设置ip代理
    myproxies = ['124.88.67.52:843','120.92.3.127:80','122.72.32.73:80','122.72.32.72:80','60.218.117.80:8118','223.244.40.174:8118','123.165.118.241:8118','121.204.165.72:8118','119.48.176.140:8118','125.118.147.179:808','120.77.169.244:8118','110.72.17.42:8123']
    proxy = random.choice(myproxies)
    proxy_support = urllib2.ProxyHandler({'http':proxy})


    content = ''
    try:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        urllib2.install_opener(opener)
        # opener = urllib2.build_opener(proxy_support)
        # urllib2.install_opener(opener)
        # response = opener.open(request)
        response = urllib2.urlopen(request,timeout=5)
        content = response.read().decode('utf-8')
        # print(response.read())
    except urllib2.URLError, e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
        print('other error!')

    # content = response.read().decode('utf-8')
    # print(content)

    # .*?(.*?<span class="cmt-name">(.*?)</span>.*?<div class="main-text">\n(.*?)<div class="likenum">.*?</a>)?(\n){4}</div>
    reStr = r'<div class="article block untagged mb15".*?<h2>(.*?)</h2>.*?<a href="/article.*?<span>(.*?)</span>.*?<span class="stats-vote"><i class="number">(.*?)</i>.*?<div class="single-clear"></div>'
    pattern = re.compile(reStr, re.S)
    items = re.finditer(pattern, content)
    i = 0
    for item in items:
        print('第%s页第%s条'%(str(pageSize),str(i)))
        i = i + 1
        item1 = item.group(1).encode('utf-8')
        item2 = item.group(2).encode('utf-8')
        item3 = item.group(3).encode('utf-8')

        regex = r'<br/>'
        reObj = re.compile(regex)
        result = reObj.subn('\n', item2)
        if result:
            item2 = result[0]

        print('作者: ' + item1)
        print('段子: ' + item2)
        print('点赞数: ' + item3)

        if item.lastindex > 3:
            # item4 = item.group(4).encode('utf-8')
            item5 = item.group(5).encode('utf-8')
            item6 = item.group(6).encode('utf-8')
            regex = r'<br/>'
            reObj = re.compile(regex)
            result = reObj.subn('\n', item6)
            if result:
                item6 = result[0]
            print('神评(%s)%s' % (item5, item6))

for page in range(1,36):
    print(str(page))
    getQsbk(page)
    # time.sleep(0.5)