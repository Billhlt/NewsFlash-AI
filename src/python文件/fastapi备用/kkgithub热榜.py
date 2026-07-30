import requests
from bs4 import BeautifulSoup
import re

#三个url，分别是：https://kkgithub.com/trending、https://github.com/trending、https://github-zh.com/trending
url = "https://kkgithub.com/trending"
headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        ,"Referer" : "https://www.baidu.com/" 
    }
response = requests.get(url, headers=headers).text

#################github项目地址#################
# 项目地址为github.com/项目作者/项目名称
# 获取项目作者和名称
pattern = r'<span data-view-component="true" class="text-normal">(.*?)</a>  </h2>'
nameinfo = re.findall(pattern,response,re.DOTALL)
# 使用 BeautifulSoup 清理内容
ghname = []
for item in nameinfo:
    # 解析HTML内容
    soup = BeautifulSoup(item, 'html.parser')
    # 提取纯文本内容并去除多余的空格和换行符
    clean_text = soup.get_text(strip=True)
    ghname.append(clean_text)

# 获取项目描述
pattern = r'<p class="col-9 color-fg-muted my-1 pr-4">(.*?)</p>'
decripsioninfo = re.findall(pattern,response,re.DOTALL)
# 使用 BeautifulSoup 清理内容
ghdescri = []
for item in decripsioninfo:
    # 解析HTML内容
    soup = BeautifulSoup(item, 'html.parser')
    # 提取纯文本内容并去除多余的空格和换行符
    clean_text = soup.get_text(strip=True)
    ghdescri.append(clean_text)








##########以下为输出代码##########
# def print_kkgithub():
#     for i in range(len(ghname)):
#         print(str(i+1)+"."+ghname[i],"\t\t",ghdesc[i])
        



        
# print_kkgithub()
# print(response)







# 以下为爬取github官网的代码，受vpn网速影响较大，故暂不使用
# url = "https://github.com/trending/"
# headers = {
#         "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
#         ,"Referer" : "https://github.com/" 
#     }
# response = requests.get(url, headers=headers).text
# # print(response.status_code)
# urlinfo = re.findall('href="(.*?)" data-view-component="true" class="Link">',response)[0]
# urlinfo = "https://github.com"+urlinfo
# print(urlinfo)
# introinfo = re.findall('</a>  </h2>(.{0,600})<div class="f6 color-fg-muted mt-2">',response,re.DOTALL)[0] # re.DOTALL表示匹配所有字符，包括换行符
# introinfo = introinfo.strip() # 去掉首尾空格和换行符
# print(introinfo)
# # print(response)


#     以下为ai写的爬虫的片段，没有意义，仅可参考其中函数
#     try:
#         response = requests.get(url, headers=headers) 
#         print(response.text)
#         response.raise_for_status()  # 检查请求是否成功
#         soup = BeautifulSoup(response.text, "html.parser")
#         print(soup)
#         # 找到包含趋势项目的容器
#         articles = soup.find_all("article", class_="Box-row")

# #         for article in articles:
# #             # 获取项目作者和项目名
# #             repo_info = article.find("h2").find_all("span")
# #             repo_author = repo_info[0].get_text(strip=True).replace(' /', '')
# #             repo_name = repo_info[1].get_text(strip=True)
# #             repo_url = "https://github.com" + article.find("h2").find("a")["href"]

# #             # 获取项目介绍
# #             repo_description = article.find("p", class_="col-9 color-fg-muted my-1 pr-4")
# #             repo_description = repo_description.get_text(strip=True) if repo_description else "No description"

# #             print(f"项目作者: {repo_author}")
# #             print(f"项目名: {repo_name}")
# #             print(f"项目介绍: {repo_description}")
# #             print(f"项目链接: {repo_url}")
# #             print("-" * 80)

#     except requests.exceptions.RequestException as e:
#          print(f"请求失败: {e}")

# if __name__ == "__main__":
#     get_github_trending()