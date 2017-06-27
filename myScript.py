#! /usr/bin/python3

import requests
from bs4 import BeautifulSoup

url = 'https://daily.zhihu.com/'

# 请求头是从chrome 中network中直接拷贝的
headers = { 'User-Agent' :
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
             'Accept'    : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
            }

# 代理来自 (http://www.xicidaili.com/nn/)
proxies = {
            'http'  : 'http://119.5.0.59',
            'https' : '123.169.84.173'
}

response = requests.get(url, headers = headers)
bsObj = BeautifulSoup(response.text, 'html.parser')
print (bsObj.body)

