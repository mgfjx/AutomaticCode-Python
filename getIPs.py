#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import BeautifulSoup
import time
import socket
socket.setdefaulttimeout(3)

def checkIPs(ip, port):
    url = 'http://www.baidu.com'
    proxys = []
    proxy_host = 'http://' + str(ip) + ':' + str(port)
    proxy_temp = {"http":proxy_host}
    proxys.append(proxy_temp)
    try:
        res = urllib.urlopen(url, proxies=proxy_temp).read()
        print('ip: %s 可用'%str(ip))
        print(res)
        return True
    except Exception,e:
        print('ip:' + str(ip) + '不可用')
        # print(e)
        return False

def getIPs(index=1):
    User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    header = {}
    header['User-Agent'] = User_Agent

    url = 'http://www.xicidaili.com/nn/'+str(index)
    req = urllib2.Request(url, headers=header)
    res = urllib2.urlopen(req).read()

    soup = BeautifulSoup.BeautifulSoup(res)
    ips = soup.findAll('tr')
    # print(ips[1])
    f = open("./ips.txt", "a")

    for x in range(1, len(ips)):
        ipModel = ips[x]
        tds = ipModel.findAll("td")
        ip = tds[1].contents[0]
        port = tds[2].contents[0]
        checkIPs(ip,port)

        # ip_temp = tds[1].contents[0] + "\t\t" + tds[2].contents[0] + "\n"
        # print(ip_temp)
        # f.write(ip_temp)

for page in range(1,32):
    getIPs(page)
    # time.sleep(0.5)