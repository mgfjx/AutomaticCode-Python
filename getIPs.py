#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import BeautifulSoup
import time
import socket
import sqlite3

def checkIPs(ip, port):
    socket.setdefaulttimeout(3)
    url = 'http://ip.chinaz.com/getip.aspx'
    userAgent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    proxy_host = str(ip) + ':' + str(port)
    req = urllib2.Request(url)
    req.add_header('User-Agent',userAgent)

    proxy_handler = urllib2.ProxyHandler({'http':proxy_host})
    proxy_auth_handler = urllib2.ProxyBasicAuthHandler()
    opener = urllib2.build_opener(proxy_handler, proxy_auth_handler)

    opener.addheaders = [('User-Agent', userAgent)]

    print(proxy_host)
    try:
        response = opener.open(url)
        response_data = response.read().decode('utf8')
        soup = BeautifulSoup.BeautifulSoup(response_data)
        content = soup.findAll('body')
        f = open("./ips.txt", "a")
        f.write(proxy_host + '\n')
        print(content)
        return True
    except Exception,e:
        # print('ip:' + str(ip) + '不可用')
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

    for x in range(1, len(ips)):
        ipModel = ips[x]
        tds = ipModel.findAll("td")
        ip = tds[1].contents[0]
        port = tds[2].contents[0]
        # checkIPs(ip,port)
        country = '中国'
        address = tds[3].contents[1].contents[0]
        print(address)
        # sql = "INSERT INTO IpList (id, country, ip, port, address, type, time) VALUES  (1, %s, %s, %s, %s, %s, %s)" % ()
        #
        # conn = sqlite3.connect('ips.db')
        # conn.execute(sql)
        # conn.commit()
        # conn.close()

def initDataBase():
    conn = sqlite3.connect('ips.db')
    print(conn)

    conn.execute('''CREATE TABLE IpList
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    country TEXT,
                    ip TEXT,
                    port TEXT,
                    address TEXT,
                    type TEXT,
                    time TEXT)
                    ''')
    conn.close()

# initDataBase()
for page in range(1,3):
    getIPs(page)
    time.sleep(0.5)