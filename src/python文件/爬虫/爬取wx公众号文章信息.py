import requests
import json
import re
from bs4 import BeautifulSoup
import pprint    
import time
import datetime
headers ={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
   ,"Referer": "https://mp.weixin.qq.com/"
   ,"cookie" : "eas_sid=C1E7Y4T8Z3h4v9u3B7l2W3L6C7; pgv_pvid=9247808219; ua_id=egOd87dhTcHQEz6vAAAAAKfhcAjnu4Hv4isbJBP_lzg=; wxuin=49733519244516; mm_lang=zh_CN; yyb_muid=3534CD11B82067032834D8E1B9F2667C; RK=j/NAMJc7MV; ptcz=a418fbc06b82bf3957c4f72d10e4cc7d30a4460768091ad355e4529d9177f262; _ga=GA1.1.1992704597.1762070983; _ga_PF3XX5J8LE=GS2.1.s1762070982$o1$g0$t1762070992$j50$l0$h0; _qimei_uuid42=19b0210093510092ae636f3e598e04d7a3b14f3bcf; _qimei_fingerprint=cb8424c1c4448d1c39cfde47cc88a2aa; _qimei_i_3=4cc95383c70e57d29596fc365ad770b3f6bca0a21b0a078be088280a2095713a336337903989e2aad088; _qimei_h38=52f7f066ae636f3e598e04d709000003819b02; _qimei_i_1=74df6487970c578dc191f8610e8270e6a1edf1f41b535682b0db2f582f93206c6163349d3980b0dcd4f3dad5; _t_qbtool_uid=aaaaqsqu77u44vshpn0grzr4dfbc88cb; _ga_TPFW0KPXC1=GS2.1.s1765343050$o1$g1$t1765343768$j60$l0$h0; uuid=19eecd06d1c9401ca38b64c8756ed0b6; _clck=3935680643|1|g5t|0; rand_info=CAESINcZlFd3WbRp0Zn5UNfgyQhfISV4al7WGI6fudXOpaIw; slave_bizuin=3935680643; data_bizuin=3935680643; bizuin=3935680643; data_ticket=BzwefZchCOyoRnFwwYonwj7zRmJMOHMQL1DmKMcK4SddNDxMYJI7YBV4SUjx3/Nh; slave_sid=TTUxY1JCZkZOeEJKc2lkVkJ4anJuR3pwYkRLMUdfVUhFdXowQjJPek5uOGVnRjZpaF9ONGNnZUpsWVFWU0Z2aFBtMUtVb0Zpcm5kTzM5ZU00U3dfbWpER3ZPd0xLdnFWRU53aXNUbGZnazRyRTFEWjhTNlQwVmdXa0UxRmt1dlNOS0hnaWQ0b2NYU21sNlZJ; slave_user=gh_25b58f0685d7; xid=9d1c164fa9033302759c5f620edb9a31; _clsk=oxzgne|1778033018611|2|1|mp.weixin.qq.com/weheat-agent/payload/record"
   ,
   
}
param ={
"search_field": "null",
"begin": "0",
"count": "5",
"query": "",
"fakeid": "Mz",
"data": "sub: list",
"IzNjc1NzUzMw==": "",
"type": "101_1",
"free_publish_type": "1",
"sub_action": "list_ex",
"lang": "zh_CN",
"f": "json",
"ajax": "1"
}
i="0"
j="5"
# token：1921924290
#################微信公众号网站（供传入print_wxoa()）
# 1.机器之心
机器之心 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzA3MzI4MjgzMw==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1921924290&lang=zh_CN&f=json&ajax=1"
# 2.量子位
量子位 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzIzNjc1NzUzMw%3D%3D&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1921924290&lang=zh_CN&f=json&ajax=1"
# 3.创业邦
创业邦 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5OTAzMjc4MA==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1921924290&lang=zh_CN&f=json&ajax=1"
# 4.新智元
新智元 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzI3MTA0MTk1MA==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1921924290&lang=zh_CN&f=json&ajax=1"
# 5.XR Vision Pro
xrvision = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5OTY1ODgxMg==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1921924290&lang=zh_CN&f=json&ajax=1"
# 6.阿里云开发者
阿里云开发者 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5OTY1ODgxMg==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1921924290&lang=zh_CN&f=json&ajax=1"
# 7.APPSO
appso = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5MjAyNDUyMA==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1921924290&lang=zh_CN&f=json&ajax=1"
# 8._36氪
_36氪 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzI2NDk5NzA0Mw==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1921924290&lang=zh_CN&f=json&ajax=1"
# 9.CodeSheep
codesheep = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzU4ODI1MjA3NQ==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1921924290&lang=zh_CN&f=json&ajax=1"
# 10.智能涌现
智能涌现 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzkwMDQ2NDU2Nw==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1921924290&lang=zh_CN&f=json&ajax=1"


# def print_wxoa(url): # oa -> Official Account
response = requests.get(url,headers=headers,params=param).text
# print(response)

pattern = r'create_time\\\\\\\":(\d{2,11}),\\\\\\\"is'
timinfo = re.findall(pattern,response) 
for i in range(len(timinfo)): 
    timinfo[i] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timinfo[i])))

pattern = r'/s\\\\\\\\\\\\/(.{1,30})\\\\\\\",\\\\\\\"digest'# 提取文章链接  
urlinfo = re.findall(pattern,response) # 提取文章链接 
for i in range(len(urlinfo)): 
    urlinfo[i]='https://mp.weixin.qq.com/s/'+urlinfo[i]
        
        
pattern = r'title\\\\\\\":\\\\\\\"(.{1,65})\\\\\\\",\\\\\\\"cover'
titleinfo = re.findall(pattern,response) 
    
##########以下为输出代码##########
    # for i in range(len(titleinfo)):
    #     print(str(i+1)+"."+titleinfo[i])
    # print("------------------------------------------------------")    
    # for i in range(len(titleinfo)):
    #     print(str(i+1)+"."+timinfo[i],"\t",urlinfo[i])

#########################核心代码#########################
# response = requests.get(url3,headers=headers,params=param).text
# # print(response)

# pattern = r'create_time\\\\\\\":(\d{2,11}),\\\\\\\"is'
# timinfo = re.findall(pattern,response) 


# pattern = r'/s\\\\\\\\\\\\/(.{1,30})\\\\\\\",\\\\\\\"digest'# 提取文章链接  
# urlinfo = re.findall(pattern,response) # 提取文章链接 
# for i in range(len(urlinfo)): 
#     urlinfo[i]='https://mp.weixin.qq.com/s/'+urlinfo[i]
    
    
# pattern = r'title\\\\\\\":\\\\\\\"(.{1,65})\\\\\\\",\\\\\\\"cover'
# titleinfo = re.findall(pattern,response) 



# # urlinfo = re.findall('" data-v-4a0a9b1c>(.{0,25})</h3></a><!----><div class="bili-video-card__info--bottom" data-v-4a0a9b1c><!',response)[0]
# print(response)


#############总结#############
# 1. cookie所有公众号通用
# 2. url中更换fakeid即更换公众号
# 3. XR vision pro更新频率有限一页最多5篇文章，多的正常13篇左右
# 4. fakeid列表：
# "MzIzNjc1NzUzMw%3D%3D"  # 量子位
# "MzA3MzI4MjgzMw=="  # 机器之心
# "MzI3MTA0MTk1MA=="  # 新智元
# "MjM5OTAzMjc4MA=="  # 创业邦
# "MjM5OTY1ODgxMg=="  # XR Vision Pro （5篇一页）
# "MjM5OTY1ODgxMg=="  # 阿里云开发者 （5）
# "MjM5MjAyNDUyMA=="  # APPSO (6)
# "MzU4ODI1MjA3NQ=="  # CodeSheep (4)
# "MzI2NDk5NzA0Mw=="  # 36氪（15）
# "MzkwMDQ2NDU2Nw=="  # 智能涌现（5）
# ""  # 
# ""  # 
# ""  # 
