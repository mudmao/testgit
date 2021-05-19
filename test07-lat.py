# encoding: utf-8

import json
from importlib import reload

import requests
from bs4 import BeautifulSoup
import re
import sys

reload(sys)


for i in range(1):
    # 循环构造url
    # url = 'http://nb.lianjia.com/ershoufang/pg{}/'
    url='https://nb.lianjia.com/ershoufang/pg{}/'
    k = url.format(i)

    # 添加请求头，否则会被拒绝
    headers = {'user-agent': 'my-app/0.0.1'}
    res = requests.get(k, headers=headers)
    # 基于正则表达式来解析网页内容，拿到所有的详情url
    # 原始可能是这么做的，但是后来发现bs4给我们提供了更方便的方法来取得各元素的内容
    # 正则表达式最重要的两个东西，.任意匹配字符，*匹配任意次数，？以html结束
    text = res.text
    # re_set = re.compile('https://nb.lianjia.com/ershoufang/[0-9]*.?html')
    re_set=re.compile('https://nb.lianjia.com/ershoufang/[0-9]*.?html')
    re_get = re.findall(re_set, text)
    print(re_get)

for name in re_get:
    res = requests.get(name, headers=headers)
    info = {}
    text2 = res.text
    # 基于bs4来解析，再也不用写正则了。
    soup = BeautifulSoup(text2, 'lxml')
    info['标题'] = soup.select('.main')[0].text
    info['总价'] = soup.select('.total')[0].text
    info['每平方售价'] = soup.select('.unitPriceValue')[0].text
    info['参考总价'] = soup.select('.taxtext')[0].text
    info['建造时间'] = soup.select('.subInfo')[2].text
    info['小区名称'] = soup.select('.info')[0].text
    info['所在区域'] = soup.select('.info a')[0].text + ':' + soup.select('.info a')[1].text
    info['链家编号'] = str(re_get)[33:].rsplit('.html')[0]

    # 根据地址获取对应经纬度，通过百度的api接口来进行
    mc = soup.select('.info')[0].text
    print(mc)
    location = '宁波' + mc
    # api_url = 'http://api.map.baidu.com/geocoder/v2/?address={}&output=json&ak=uGWhzTXoh4LEigsZnYQa84M09dEYgETw'.format(location)
    api_url='http://api.map.baidu.com/reverse_geocoding/v3/?ak=Gv2Y0KTNMec26hR8eE4LdwYSv4SlwTGA&output=json&coordtype=wgs84ll&location=31.225696,121.49884'.format(location)
    data = requests.get(api_url)
    result = json.loads(data.text)
    try:
        longitude = result['result']['location']['lng']
        latitude = result['result']['location']['lat']
    except Exception as e:
        print('Error:这个地点没有查到对应的经纬度---- %s' % str(e))
        longitude = [0]
        latitude = [0]
k = 1