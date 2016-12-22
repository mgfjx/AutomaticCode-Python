#coding:utf-8
import urllib2
import random
import requests

def get_html(url,headers,proxies):

    random_userAget = random.choice(headers)
    random_proxy = random.choice(proxies)

    #下面是模拟浏览器进行访问
    req = urllib2.Request(url)
    print(url)
    req.add_header("User-Agent", random_userAget)

    #下面是使用ip代理进行访问
    # proxy_support = urllib2.ProxyHandler({"http":random_proxy})
    # opener = urllib2.build_opener(proxy_support)
    # urllib2.install_opener(opener)


    html = urllib2.urlopen(req)
    return html

url = "http://news.163.com/world/"
user_agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36']
#网上的ip有可能是不能用的，需要多做尝试
myproxies=['112.25.222.170']

# url = url + str(1)
html = get_html(url,user_agents,myproxies)
print(html.read())
quit()

for i in range(1, 1000000):
    url = url + str(i)
    html = get_html(url,user_agents,myproxies)
    print(html.read())
    if html:
        print('第%s次'%str(i))