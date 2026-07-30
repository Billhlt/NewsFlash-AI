import requests
import json
import re
from bs4 import BeautifulSoup
import pprint    
import time
headers ={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
   ,"Referer": "https://www.bilibili.com/"
}

# url = "https://search.bilibili.com/all?keyword=lks&from_source=webtop_search&spm_id_from=333.1007&search_source=4"
# response = requests.get(url,headers=headers).text
# 正则搜索关键词 <span class="ml_0 bili-video-card__info--date" data-v-4a0a9b1c
# print(response)





###############输入精确up名称循环打印up最新视频标题和日期与链接###############
# def print_up_video(name:str) -> None:
    
url = "https://search.bilibili.com/all?keyword="+name
response = requests.get(url,headers=headers).text
bupdate = re.findall('<span class="ml_0 bili-video-card__info--date" data-v-(.*?)</span>',response)# 共有八条视频数据
buptitle = re.findall('" data-v-(.{0,81})</h3></a><!----><div class="bili-video-card__info--bottom" data-v-',response)
for b in range(8):
    j=0
    for i in range(len(bupdate[b])):
        if bupdate[b][i] == ">":
            j=i
            break
    bupdate[b] = bupdate[b][j+1:]
    for i in range(len(buptitle[b])):
        if buptitle[b][i] == ">":
            j=i
            break
    buptitle[b] = buptitle[b][j+1:]
#     print(buptitle)   
  
##########以下为输出代码##########
# for a in range(8):
#     print(buptitle[a])
#     print(bupdate[a])
# print("url:",url)


# print_up_video("周鸿祎")







###################以下为核心代码###################
# a=0
# bupdate = re.findall('<span class="ml_0 bili-video-card__info--date" data-v-(.*?)</span>',response)[a]# 共有八条视频数据
# for i in range(len(bupdate)):
#     if bupdate[i] == ">":
#         j=i
#         break;
# bupdate = bupdate[j+1:]
# print(bupdate)



# b=0
# buptitle = re.findall('" data-v-(.{0,38})</h3></a><!----><div class="bili-video-card__info--bottom" data-v-',response)[b]
# for i in range(len(buptitle)):
#     if buptitle[i] == ">":
#         j=i
#         break;
# buptitle = buptitle[j+1:]
# print(buptitle)



# 以下为爬取动态网页但是因url动态更新而无法持续爬取的代码
# url = "https://api.bilibili.com/x/space/wbi/arc/search?pn=2&ps=40&tid=0&special_type=&order=pubdate&mid=385670211&index=0&keyword=&order_avoided=true&platform=web&web_location=333.1387"
# response = requests.get(url,headers=headers).text
# # print(response.text)
# json_data = json.loads(response)
# # print(json_data)
# title = json_data['data']['list']['vlist'][0]['title']
# bvid = json_data['data']['list']['vlist'][0]['bvid']
# tim = json_data['data']['list']['vlist'][0]['created'] # time为时间戳
# rtim = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tim)) # 将时间戳转换为时间
# print(rtim)