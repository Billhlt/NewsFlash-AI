import requests
from bs4 import BeautifulSoup
import re
import json

# 以下为爬取app网页版b站热搜的代码
url = "https://app.bilibili.com/x/v2/search/trending/ranking?csrf=45735bafe7cb3edcf0fddbd3a4e74e36&limit=30"
headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        
    }
# 30+1个热搜，1为红色置顶新闻
response = requests.get(url, headers=headers).text
json_data=json.loads(response) 
bseartitle = []
for i in range(30):
    bseartitle.append(json_data['data']['list'][i]['show_name'])
bseartitle.append('https://search.bilibili.com/all?keyword=')
# print(response.status_code)


# 以下为单次赋值并输出热搜名称和链接的代码
# i=0
# bseartitle = json_data['data']['list'][i]['show_name']
# urlinfo = "https://search.bilibili.com/all?keyword="+bseartitle
# print(bseartitle)
# print(urlinfo)

######################循环打印热搜名称和链接######################
# def print_bilihot():
#     print()
#     print("#######################b站热搜榜#######################")
#     for i in range(30):
#         bseartitle = json_data['data']['list'][i]['show_name']
#         urlinfo = "https://search.bilibili.com/all?keyword="+bseartitle
#         print(bseartitle,'\t\t\t', urlinfo)

# print_info()
# print(introinfo)
# print(response)








# print_info()
# print(introinfo)
# print(response)



















