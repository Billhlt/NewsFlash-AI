import re
import requests
from datetime import datetime, timedelta
from tqdm import tqdm

# 全局变量，用于缓存数据
display_ph = []
display_phurls = []

def fetch_producthunt_data():
    """获取并解析 ProductHunt 热榜数据"""
    global display_ph, display_phurls
    
    try:
        # 获取昨天的日期
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_str = yesterday.strftime('%Y-%m-%d')
        
        url = 'https://decohack.com/producthunt-daily-' + yesterday_str + '/'
        
        # 执行网络请求
        response = requests.get(url, timeout=50).text
        
        titles, slogans, intros, prod_links, ph_links, votes = [], [], [], [], [], []
        
        # 使用正则表达式提取标题
        title_pattern = r'<h2>.*?<a[^>]*>(.*?)</a></h2>'
        titles_raw = re.findall(title_pattern, response, re.DOTALL)
        for title in titles_raw:
            # 去掉前面的序号 "1. "、"2. "……
            clean_title = re.sub(r'^\d+\.\s*', '', title.strip())
            titles.append(clean_title)
        
        # 使用正则表达式提取产品块
        product_blocks = re.findall(r'<h2>.*?</h2>(.*?)<p><img', response, re.DOTALL)
        
        for block in product_blocks:
            # 标语
            slogan_match = re.search(r'<strong>标语</strong>：(.*?)<br />', block)
            slogan = slogan_match.group(1).strip() if slogan_match else ''
            slogans.append(slogan)
            
            # 介绍
            intro_match = re.search(r'<strong>介绍</strong>：(.*?)(?:<br/?>|<strong>)', block, re.DOTALL)
            intro = re.sub(r'<.*?>', '', intro_match.group(1)).strip() if intro_match else ''
            intros.append(intro)
            
            # 产品网站
            prod_match = re.search(r'<strong>产品网站</strong>: <a href="(.*?)"', block)
            prod_link = prod_match.group(1).strip() if prod_match else ''
            prod_links.append(prod_link)
            
            # Product Hunt 网站
            ph_match = re.search(r'<strong>Product Hunt</strong>: <a href="(.*?)"', block)
            ph_link = ph_match.group(1).strip() if ph_match else ''
            ph_links.append(ph_link)
        
        # 票数
        pattern = r'<strong>票数</strong>: 🔺(.*?)<br />'
        votes = re.findall(pattern, response)
        
        # 整合数据
        display_ph = []
        display_phurls = []
        # 全显示：display_ph.append(f"@@@{i+1}.标题：{titles[i]}\n标语：{slogans[i]}\n介绍：{intros[i]}\n产品网站：{prod_links[i]}\nProduct Hunt 网站：{ph_links[i]}\n票数：{votes[i]}\n\n")
        for i in tqdm(range(min(30, len(titles))), desc="整合producthunt热榜"):
            if i < len(titles):
                display_ph.append(f"{i+1}.标题：{titles[i]}<br>标语：{slogans[i]}<br>介绍：{intros[i]}<br>票数：{votes[i] if i < len(votes) else 'N/A'}")
                display_phurls.append(prod_links[i] if i < len(prod_links) else '')
        
        return display_ph, display_phurls
    
    except Exception as e:
        print(f"获取 ProductHunt 数据失败: {e}")
        # 返回空列表，避免应用崩溃
        return [], []

# 初始化时获取数据（可选，如果希望启动时就加载数据）
# fetch_producthunt_data()
