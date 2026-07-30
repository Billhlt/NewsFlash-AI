import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

# 全局变量，用于缓存数据
ghname = []
ghdescri = []
display_gh = []

def fetch_github_trending():
    """获取并解析 GitHub 热榜数据"""
    global ghname, ghdescri, display_gh
    
    try:
        #三个url，分别是：https://kkgithub.com/trending、https://github.com/trending、https://github-zh.com/trending
        # 月榜：https://github.com/trending?since=monthly
        # 周榜：https://github.com/trending?since=weekly
        # 日榜：https://github.com/trending?since=daily
        url = "https://github.com/trending?since=daily"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Referer": "https://www.baidu.com/",
            "Cookie": "_gh_sess=3HN80ueYD7IPOkgZnwQCqVsd7660FBcjUGGFE26qhUZXCJh48vmB0F%2FVcY4g4yKk5vTdfekQcWiFmanpL1nkszCbJMzeT%2BpnQjGAYe6fSdbFh7sCqpceFxHBNujeTwU4MvREuk1g5Tm6JOmmc9sjU1Ixxw%2BDG5flGiEwFglNrd6snkqyiiGicjqWlLvS0hKok3Zgcs0gThNxfMAI7Pd2y%2BGurcTtPd88pkVbiaUc3HmnidHJysG587qppczr%2FbMwWYc7KqYle4fmrYMeN%2BlsKQ%3D%3D--M3TsIQFP7uvSEX4D--BQlBpDhtQt2HLxBooVUi7A%3D%3D; _octo=GH1.1.2058701624.1757464753; logged_in=no; cpu_bucket=xlg; preferred_color_mode=light; tz=Asia%2FShanghai"
        }
        
        respons = requests.get(url, headers=headers)
        response = respons.text
        
        #################github项目地址#################
        # 项目地址为github.com/项目作者/项目名称
        # 获取项目作者和名称
        pattern = r'<span data-view-component="true" class="text-normal">(.*?)</a>  </h2>'
        nameinfo = re.findall(pattern, response, re.DOTALL)
        # 使用 BeautifulSoup 清理内容
        ghname = []
        for item in nameinfo:
            # 解析HTML内容
            soup = BeautifulSoup(item, 'html.parser')
            # 提取纯文本内容并去除多余的空格和换行符
            clean_text = soup.get_text(strip=True)
            # 去除字符串中间的所有空格
            clean_text = clean_text.replace(' ', '')
            ghname.append(clean_text)
        
        # 获取项目描述
        pattern = r'</a>  </h2>(.*?)<div class="f6 color-fg-muted mt-2">'
        decripsioninfo = re.findall(pattern, response, re.DOTALL)
        # 使用 BeautifulSoup 清理内容
        ghdescri = []
        for item in decripsioninfo:
            # 解析HTML内容
            soup = BeautifulSoup(item, 'html.parser')
            # 提取纯文本内容并去除多余的空格和换行符
            clean_text = soup.get_text(strip=True)
            ghdescri.append(clean_text)
        
        pattern = r'<svg aria-label="star" role="img" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-star">(.*?)</a>'
        ghstarinfo = re.findall(pattern, response, re.DOTALL)
        # 使用 BeautifulSoup 清理内容
        ghstar = []
        for item in ghstarinfo:
            # 解析HTML内容
            soup = BeautifulSoup(item, 'html.parser')
            # 提取纯文本内容并去除多余的空格和换行符
            clean_text = soup.get_text(strip=True)
            ghstar.append(clean_text)
        
        pattern = r'<svg aria-label="fork" role="img" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-repo-forked">(.*?)</span>'
        ghforkinfo = re.findall(pattern, response, re.DOTALL)
        # 使用 BeautifulSoup 清理内容
        ghfork = []
        for item in ghforkinfo:
            # 解析HTML内容
            soup = BeautifulSoup(item, 'html.parser')
            # 提取纯文本内容并去除多余的空格和换行符
            clean_text = soup.get_text(strip=True)
            # 去除末尾的'Built by'
            if clean_text.endswith('Built by'):
                clean_text = clean_text[:-len('Built by')].rstrip()
            ghfork.append(clean_text)
        
        pattern = r'<span data-view-component="true" class="d-inline-block float-sm-right">(.*?)</span>'
        ghstar_todayinfo = re.findall(pattern, response, re.DOTALL)
        # 使用 BeautifulSoup 清理内容
        ghstar_today = []
        for item in ghstar_todayinfo:
            # 解析HTML内容
            soup = BeautifulSoup(item, 'html.parser')
            # 提取纯文本内容并去除多余的空格和换行符
            clean_text = soup.get_text(strip=True)
            # 去除末尾的' stars today'
            if clean_text.endswith(' stars today'):
                clean_text = clean_text[:-len(' stars today')].rstrip()
            ghstar_today.append(clean_text)
        
        # 整合数据
        display_gh = []
        for i in tqdm(range(len(ghdescri)), desc="整合github热榜"):
            if i < len(ghname) and i < len(ghstar) and i < len(ghfork) and i < len(ghstar_today):
                display_gh.append(f"{i+1}.项目名：{ghname[i]}<br>描述：{ghdescri[i]}<br>star：{ghstar[i]}<br>fork：{ghfork[i]}<br>star_today：{ghstar_today[i]}")
        
        return display_gh, ghname
    
    except Exception as e:
        print(f"获取 GitHub 数据失败: {e}")
        # 返回空列表，避免应用崩溃
        return [], []

# 初始化时获取数据（可选，如果希望启动时就加载数据）
# fetch_github_trending()
