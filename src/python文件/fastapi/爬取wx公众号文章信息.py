import requests
import json
import re
from bs4 import BeautifulSoup
import pprint    
import time
import datetime
from tqdm import tqdm


headers ={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
   ,"Referer": "https://mp.weixin.qq.com/"
   ,"cookie" : "pgv_pvid=9247808219; ua_id=egOd87dhTcHQEz6vAAAAAKfhcAjnu4Hv4isbJBP_lzg=; wxuin=49733519244516; mm_lang=zh_CN; yyb_muid=3534CD11B82067032834D8E1B9F2667C; RK=j/NAMJc7MV; ptcz=a418fbc06b82bf3957c4f72d10e4cc7d30a4460768091ad355e4529d9177f262; _ga=GA1.1.1992704597.1762070983; _ga_PF3XX5J8LE=GS2.1.s1762070982$o1$g0$t1762070992$j50$l0$h0; _qimei_uuid42=19b0210093510092ae636f3e598e04d7a3b14f3bcf; _qimei_fingerprint=cb8424c1c4448d1c39cfde47cc88a2aa; _qimei_i_3=4cc95383c70e57d29596fc365ad770b3f6bca0a21b0a078be088280a2095713a336337903989e2aad088; _qimei_h38=52f7f066ae636f3e598e04d709000003819b02; _qimei_i_1=74df6487970c578dc191f8610e8270e6a1edf1f41b535682b0db2f582f93206c6163349d3980b0dcd4f3dad5; _t_qbtool_uid=aaaaqsqu77u44vshpn0grzr4dfbc88cb; _ga_TPFW0KPXC1=GS2.1.s1765343050$o1$g1$t1765343768$j60$l0$h0; _clck=3935680643|1|g7q|0; uuid=7c32d75e58e85d32df4d89b90af7b51d; rand_info=CAESILAxchbNi4p21Wiq0d8m/yssu5kXjb80zFtb/pA9tlp2; slave_bizuin=3935680643; data_bizuin=3935680643; bizuin=3935680643; data_ticket=YQ3sPpCxbr8zM/L6G4wWPWSdw73UNgZrSOMx0YZO30bWFWKXkQD9p4wjramMmNre; slave_sid=OXljS0JzT1B2ek1qNXJVVTFIb0lsaGc3ZmlxWHp5VjZhdXBzSnZHemloNzlBM1RQeURadHc0MHl5MFpESFduTk9meWJRaU82YXU1N1Nlb2R3TUNTaEkwc01wQ1B2QkZJd3lsTmJMVWRrbEV2WjhFUWEzRVhtdm9Xc1Rhc09wWGhaUkJ0ZnkyZmRpQmV1M2w1; slave_user=gh_25b58f0685d7; xid=b88778b62a1bdb676cb7d4b7495b55ee; _clsk=17v768|1784013135748|2|1|mp.weixin.qq.com/weheat-agent/payload/record"
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
# token：275714767
#################微信公众号网站（供传入add_wxurl()）
# 1.机器之心  更新时间：每日 8点半 --18点 最多日均12
机器之心 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzA3MzI4MjgzMw==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=275714767&lang=zh_CN&f=json&ajax=1"
# 2.量子位  更新时间：每日 9点 -- 19点  （文章时多时少） 最多日均10
量子位 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzIzNjc1NzUzMw%3D%3D&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=275714767&lang=zh_CN&f=json&ajax=1"
# 3.创业邦  更新时间：每日 8点半 -- 19点半  日均11
创业邦 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5OTAzMjc4MA==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=275714767&lang=zh_CN&f=json&ajax=1"
# 4.新智元  更新时间：每日 8点 -- 22点半  日均8 最多日均12 （偶尔出现因为第二天爬取的第一页文章仅有8个，导致第一天填的12造成报错）
新智元 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzI3MTA0MTk1MA==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=275714767&lang=zh_CN&f=json&ajax=1"
# 5.XR Vision Pro  更新时间：（文章数太少） 最多日均3
xrvision = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5OTY1ODgxMg==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=275714767&lang=zh_CN&f=json&ajax=1"
# 6.阿里云开发者  更新时间：（文章数太少）日均1.5
阿里云开发者 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5OTY1ODgxMg==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=275714767&lang=zh_CN&f=json&ajax=1"
# 7.APPSO  更新时间：（文章数太少） 日均3.5
appso = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5MjAyNDUyMA==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=275714767&lang=zh_CN&f=json&ajax=1"
# 8._36氪  更新时间：每日 7点半 -- 22点半 最多日均15
_36氪 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzI2NDk5NzA0Mw==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=275714767&lang=zh_CN&f=json&ajax=1"
# 9.CodeSheep  更新时间：（文章数极其少）
codesheep = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzU4ODI1MjA3NQ==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=275714767&lang=zh_CN&f=json&ajax=1"
# 10.智能涌现  更新时间：（文章数太少）日均0.7（时无文章时2篇文章）
智能涌现 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzkwMDQ2NDU2Nw==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=275714767&lang=zh_CN&f=json&ajax=1"
# 11.极客公园  更新时间： 日均5篇
极客公园 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MTMwNDMwODQ0MQ%3D%3D&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=7d9a41aecb74344042c2ebd24de90c5d&token=275714767&lang=zh_CN&f=json&ajax=1"
FounderPark = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=Mzg5NTc0MjgwMw%3D%3D&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=7d9a41aecb74344042c2ebd24de90c5d&token=275714767&lang=zh_CN&f=json&ajax=1"
硬氪 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzkwMTI4MjU0Mw%3D%3D&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=7d9a41aecb74344042c2ebd24de90c5d&token=275714767&lang=zh_CN&f=json&ajax=1"
_36氪pro = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzUxOTA3MzMzOQ%3D%3D&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=7d9a41aecb74344042c2ebd24de90c5d&token=275714767&lang=zh_CN&f=json&ajax=1"
暗涌waves = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=Mzk0MDMyNDUxOQ%3D%3D&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=7d9a41aecb74344042c2ebd24de90c5d&token=275714767&lang=zh_CN&f=json&ajax=1"
量子位智库 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzUzNDUyNzYzNg%3D%3D&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=7d9a41aecb74344042c2ebd24de90c5d&token=275714767&lang=zh_CN&f=json&ajax=1"





aaa=''
wxurl=[]

def deserialize_response(response_text):
    """
    反序列化经过多次序列化的 JSON 字符串
    递归地调用 json.loads() 直到无法再解析
    返回反序列化后的字符串格式（便于后续正则表达式处理）
    """
    def _deserialize_recursive(obj, depth=0, max_depth=20):
        """递归反序列化函数"""
        if depth >= max_depth:
            # 如果超过最大深度，返回原对象
            return obj
        
        # 如果是字符串，尝试解析
        if isinstance(obj, str):
            try:
                parsed = json.loads(obj)
                # 解析成功，继续递归处理
                return _deserialize_recursive(parsed, depth + 1, max_depth)
            except (json.JSONDecodeError, TypeError):
                # 无法解析，返回原字符串
                return obj
        
        # 如果是字典，递归处理每个值
        elif isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                result[key] = _deserialize_recursive(value, depth + 1, max_depth)
            return result
        
        # 如果是列表，递归处理每个元素
        elif isinstance(obj, list):
            result = []
            for item in obj:
                result.append(_deserialize_recursive(item, depth + 1, max_depth))
            return result
        
        # 其他类型（int, float, bool, None），直接返回
        else:
            return obj
    
    try:
        # 先递归反序列化
        result = _deserialize_recursive(response_text)
        # 最终将结果转换为 JSON 字符串（正常格式，无多余转义）
        if isinstance(result, str):
            # 如果结果还是字符串，尝试最后一次解析
            try:
                final_parsed = json.loads(result)
                return json.dumps(final_parsed, ensure_ascii=False)
            except:
                return result
        else:
            return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        print(f"反序列化失败: {e}")
        return response_text




def add_wxurl(url): # lwxurl -> long wxurl
    response = requests.get(url,headers=headers,params=param).text
    # 反序列化 response（去除多余的转义）
    respons = deserialize_response(response)
    respons = json.loads(respons)
    # print(respons)
    len01 = len(respons['publish_page']['publish_list'])
    len02 = []
    for i in range(len01):
        len02.append(len(respons['publish_page']['publish_list'][i]['publish_info']['appmsgex']))
    for i in range(len01):
        for j in range(len02[i]):
            # 获取时间戳并转换为日期
            timestamp = respons['publish_page']['publish_list'][i]['publish_info']['appmsgex'][j]['update_time']
            # .date() 将时间截取年月日，不包含时分秒
            timestamp_date = datetime.datetime.fromtimestamp(timestamp).date()
            # 用今天的日期减去1天得到昨天的日期，下面三个数据均不包含时分秒
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            # 如果日期是昨天，则添加到wxurl列表
            if timestamp_date == yesterday: # 昨天
                wxurl.append(respons['publish_page']['publish_list'][i]['publish_info']['appmsgex'][j]['link'])

    print(f"len(wxurl): {len(wxurl)}")
    # print(f"wxurl: {wxurl}")

# add_lwxurl(量子位)







# #  每页文章数量：量子位 8-11 新智元 8-12 机器之心 8-12 创业邦 10-12 _36氪 10-15
# # 9.20 量子位 11/1 新智元 8/1 机器之心 12/5 创业邦 19/8 _36氪 18/4
# # 9.26 量子位 0 新智元 3 机器之心 0 创业邦 4 _36氪 4
#2025.12.13 公众号事故，新智元连续发了多篇重复文章，重复的文章达到20+，故今日不爬取新智元，之前要记得添加.
accounts = [(量子位), (新智元), (机器之心), (创业邦), (_36氪),(xrvision),(智能涌现),(极客公园),(FounderPark),(硬氪),(_36氪pro),(暗涌waves),(量子位智库)]    
# , (新智元), (机器之心), (创业邦), (_36氪),(xrvision),(智能涌现),(极客公园),(FounderPark),(硬氪),(_36氪pro),(暗涌waves),(量子位智库)
account_names = ["量子位", "新智元", "机器之心", "创业邦", "36氪","xrvision","智能涌现","极客公园","FounderPark","硬氪","36氪pro","暗涌waves","量子位智库"]
# , "新智元", "机器之心", "创业邦", "36氪","xrvision","智能涌现","极客公园","FounderPark","硬氪","36氪pro","暗涌waves","量子位智库"
pbar = tqdm(zip(accounts, account_names), total=len(accounts), desc="爬取wx文章url链接")
for account, name in pbar:
    pbar.set_description(f"爬取wx文章url链接 - {name}")
    add_wxurl(account)

# for循环执行完成后才执行以下代码

# print(f"wxurl: {wxurl}")
# print(f"len(wxurl): {len(wxurl)}")










##################以下为自定义爬取文章数量版式的函数##################
# def add_wxurl(url, num): # oa -> Official Account
#     response = requests.get(url,headers=headers,params=param).text
#     # print(response)

#     # pattern = r'create_time\\\\\\\":(\d{2,11}),\\\\\\\"is'
#     # wxtim = re.findall(pattern,response) 
#     # for i in range(len(wxtim)): 
#     #     wxtim[i] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(wxtim[i])))

#     pattern = r'/s\\\\\\\\\\\\/(.{1,30})\\\\\\\",\\\\\\\"digest'# 提取文章链接  
#     wxur = re.findall(pattern,response) # 提取文章链接 
#     for i in range(num):     # 如果len(wxur)=5,则依次地 i=0,1,2,3,4
#         wxur[i]='https://mp.weixin.qq.com/s/'+wxur[i]
#         wxurl.append(wxur[i])
        
#     # pattern = r'title\\\\\\\":\\\\\\\"(.{1,65})\\\\\\\",\\\\\\\"cover'
#     # wxtitle = re.findall(pattern,response) 1

# #  量子位 8-11 新智元 8-12 机器之心 8-12 创业邦 10-12 _36氪 10-15
# accounts = [(量子位, 10), (新智元, 7), (机器之心, 10), (创业邦, 12), (_36氪, 12), (智能涌现, 2), (xrvision, 3)]
# account_names = ["量子位", "新智元", "机器之心", "创业邦", "36氪", "智能涌现", "xrvision"]

# for (account, num), name in tqdm(zip(accounts, account_names), total=len(accounts), desc="爬取wx文章url链接"):
#     add_wxurl(account, num)


    # print("####################### wxoa 量子位addurl ok #######################")
    # add_wxurl(量子位)
    # print("####################### wxoa 新智元addurl ok #######################")
    # add_wxurl(新智元)
    # print("####################### wxoa 机器之心addurl ok #######################")
    # add_wxurl(机器之心)
    # print("####################### wxoa 创业邦addurl ok #######################")
    # add_wxurl(创业邦)
    # print("####################### wxoa 36氪addurl ok #######################")
    # add_wxurl(_36氪)
    # print("####################### wxoa 阿里云开发者addurl ok #######################")
    # add_wxurl(阿里云开发者)
    # print("####################### wxoa 智能涌现addurl ok #######################")
    # add_wxurl(智能涌现)


##########以下为输出代码##########
    # for i in range(len(wxtitle)):
    #     print(str(i+1)+"."+wxtitle[i])
    # print("------------------------------------------------------")    
    # for i in range(len(wxtitle)):
    #     print(str(i+1)+"."+wxtim[i],"\t",wxurl[i])

#########################核心代码#########################
# response = requests.get(url3,headers=headers,params=param).text
# # print(response)

# pattern = r'create_time\\\\\\\":(\d{2,11}),\\\\\\\"is'
# wxtim = re.findall(pattern,response) 


# pattern = r'/s\\\\\\\\\\\\/(.{1,30})\\\\\\\",\\\\\\\"digest'# 提取文章链接  
# wxURL = re.findall(pattern,response) # 提取文章链接 
# for i in range(len(wxurl)): 
#     wxurl[i]='https://mp.weixin.qq.com/s/'+wxurl[i]
    
    
# pattern = r'title\\\\\\\":\\\\\\\"(.{1,65})\\\\\\\",\\\\\\\"cover'
# wxtitle = re.findall(pattern,response) 



# # wxurl = re.findall('" data-v-4a0a9b1c>(.{0,25})</h3></a><!----><div class="bili-video-card__info--bottom" data-v-4a0a9b1c><!',response)[0]
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
