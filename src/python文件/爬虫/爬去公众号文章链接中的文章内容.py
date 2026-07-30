import requests
import re
from bs4 import BeautifulSoup
# 目标URL
url = "https://mp.weixin.qq.com/s/tVAOdjL7WVGwXyE2rXyusA"
headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
  #      ,"Referer" : "https://www.bilibili.com/blackboard/activity-trending-topic.html" 
  #      ,"Referer" : "https://www.bilibili.com/blackboard/activity-trending-topic.html" 
  #      ,"Referer" : "https://www.bilibili.com/blackboard/activity-trending-topic.html" 
        ,"Cookie" : "eas_sid=C1E7Y4T8Z3h4v9u3B7l2W3L6C7; pgv_pvid=9247808219; ua_id=egOd87dhTcHQEz6vAAAAAKfhcAjnu4Hv4isbJBP_lzg=; wxuin=49733519244516; mm_lang=zh_CN; yyb_muid=3534CD11B82067032834D8E1B9F2667C; _clck=3935680643|1|fy4|0; rand_info=CAESIC+LHuZiu2piMcraUI87LjWOzNfvC676Kwp2FwuhABPp; slave_bizuin=3935680643; data_bizuin=3935680643; bizuin=3935680643; data_ticket=hY+Xbi1/eA16LtuP0mAvGXYZoaO0qHscCE+woiMYDL9O9jrVNqqf/F7P2MM7d7g3; slave_sid=ZEtvVDhFWmtaM0NIYkZKbjRyQ21uZWJaREhveVkwazdBSUtKV3pGaDU0TWIzRXZYVW1oaGpaaks2NHA4c1puSERjalVwOTRETGtEdWJyeWEyb3VzNlQ0S2VLbVBHbTBQQkQ0U2xFZWNVRThOVXhNdjh5VVBJSEJFR3JlbWx1eDdxTE9RdzdIbGtoY09la2tp; slave_user=gh_25b58f0685d7; xid=63b76499cce0c5ca569a4871574c1332; _clsk=mk0we5|1754127625085|3|1|mp.weixin.qq.com/weheat-agent/payload/record; poc_sid=HKPIjmijKPVzWNIQHLCY2TsxCTFVCrpYEBFu5vRp; rewardsn=; wxtokenkey=777" 
    }
# 发送HTTP请求获取网页内容
response = requests.get(url, headers=headers)
# 检查请求是否成功
if response.status_code == 200:
    # 获取网页的全部源代码
    html_content = response.text
    # 定义正则表达式模式，用于匹配 <span leaf=""> 标签中的内容
    pattern = r'id="js_content" style="visibility: hidden; opacity: 0; ">(.*?)<mp-style-type data-value='

    # 使用正则表达式查找所有匹配的内容
    matches = re.findall(pattern, html_content, re.DOTALL)

    # 提取匹配的内容并拼接成一个字符串
    extracted_content = ''.join(matches)

    # 使用BeautifulSoup进行二次清理
    soup = BeautifulSoup(extracted_content, 'html.parser')
    clean_content = soup.get_text()
    
    # 清理多余空白
    clean_content = ' '.join(clean_content.split())
    
    print(clean_content)
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)




