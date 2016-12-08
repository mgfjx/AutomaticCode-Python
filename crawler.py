#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import re

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0)'
headers = {'User-Agent' : user_agent}

try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    # print(response.read())
except urllib2.URLError,e:
    if hasattr(e, 'code'):
        print(e.code)
    if hasattr(e, 'reason'):
        print(e.reason)

content = response.read().decode('utf-8')
# print(content)

# <span class="cmt-name">(.*?)</span>.*?<div class="main-text">\n(.*?)<div class="likenum">.*?
reStr = r'<div class="article block untagged mb15".*?<h2>(.*?)</h2>.*?<a href="/article.*?<span>(.*?)</span>.*?<span class="stats-vote"><i class="number">(.*?)</i>.*?<div class="single-clear"></div>.*?(.*?<span class="cmt-name">(.*?)</span>.*?<div class="main-text">\n(.*?)<div class="likenum">.*?</a>)?.*?</div>'
pattern = re.compile(reStr, re.S)
items = re.finditer(pattern, content)
i = 0
for item in items:
    print(str(i))
    i = i + 1
    print('作者: ' + item.group(1).encode('utf-8'))
    print('段子: ' + item.group(2).encode('utf-8') + '\n点赞数: ' + item.group(3).encode('utf-8'))
    if item.lastindex > 3:
        print('神评(%s)%s'%(item.group(5).encode('utf-8'),item.group(6).encode('utf-8')))
    # print(item[0],item[1],item[2],item[3],item[4])
