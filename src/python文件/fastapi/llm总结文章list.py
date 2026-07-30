import requests
from typing import List
from 爬取公众号文章链接中的文章内容2 import wxarticles
from 爬取wx公众号文章信息 import wxurl
from tqdm import tqdm
from prompt import 文章总结提示词
from prompt import 自动记笔记提示词
from prompt import 测试长文章
import concurrent.futures
# from github热榜 import display_gh
# from 爬取producthunt热榜 import display_ph
def process_article(idx: int, raw: str, endpoint: str) -> str:
    """处理单篇文章的函数，用于并发执行"""
    prompt = 自动记笔记提示词 + f"\n{raw}"
    print(prompt)
    params = {
        "prompt": prompt,
        "chatId": str(idx)
    }
    resp = requests.post(endpoint, json=params, timeout=100)
    resp.raise_for_status()
    return resp.text.strip()

def optimize_articles(articles: List[str],
                      endpoint: str = "http://localhost:8081/ai/chat",
                      max_workers: int = 200) -> List[str]:
    """ 
    对 articles 列表中的每篇文章调用本地 LLM 进行优化。
    第 i 篇文章使用 chatId = i（从 1 开始）。
    返回与输入顺序一一对应的优化后文章列表。
    使用线程池实现并发请求。
    """
    optimized = [None] * len(articles)  # 预分配结果列表
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_index = {
            executor.submit(process_article, idx, raw, endpoint): idx-1
            for idx, raw in enumerate(articles, start=1)
        }
        
        # 使用tqdm显示进度
        with tqdm(total=len(articles), desc="并发总结提取wx文章内容") as pbar:
            for future in concurrent.futures.as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    optimized[index] = future.result()
                except Exception as e:
                    print(f"处理第{index+1}篇文章时出错: {str(e)}")
                    optimized[index] = ""  # 出错时返回空字符串
                pbar.update(1)
    
    return optimized

# wxarticles为正式使用，测试文章为测试使用
总结内容list = optimize_articles(wxarticles)

# 1. 找出所有以 '@@@' 开头的元素在列表中的位置：（list_idx: 带标记的位置列表）
list_idx = [i for i, item in enumerate(总结内容list) if isinstance(item, str) and item.startswith('@@@')]

# 2. 将列表分成两部分：以 '@@@' 开头的元素和其他元素，保持原有顺序（list_marked01: 带标记的元素列表，list_unmarked01: 其他元素列表。 通过代码'item[3:]'去除了每个元素开头的'@@@'
list_marked01 = [item[3:] for item in 总结内容list if isinstance(item, str) and item.startswith('@@@')]
list_unmarked01 = [item for item in 总结内容list if not (isinstance(item, str) and item.startswith('@@@'))]



#在文章末尾补充链接（文章链接为wxurl）
# for i in tqdm(range(len(总结内容list)), desc="补充文章链接至末尾"):
#     总结内容list[i]+="\n文章链接为："
#     总结内容list[i]+=wxurl[i]

# 总结内容list.append(display_ph)
# 总结内容list.append(display_gh)


# print(总结内容list)
# 现在 optimized_articles 就是优化后的字符串列表
# for art in optimized_articles:
#     print(art, "\n" + "-"*40)
