
import re
import requests
import time
from bs4 import BeautifulSoup
from 爬取wx公众号文章信息 import wxurl
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# URL = "https://mp.weixin.qq.com/s/JQZpNgaFoivwR9fL_k-Aow"
# testurl = ["https://mp.weixin.qq.com/s/7ROi7epFms0S38OajEWFDA","https://mp.weixin.qq.com/s/lNiivIN3QyB6kr9zWr8VFA","https://mp.weixin.qq.com/s/_dfHk0IjYsYkDvIxZ02Rmw"]
testurl = ["https://mp.weixin.qq.com/s/7ROi7epFms0S38OajEWFDA"]

# 创建带重试机制的session
def create_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,  # 总共重试3次
        backoff_factor=1,  # 重试间隔：1秒、2秒、4秒
        status_forcelist=[429, 500, 502, 503, 504],  # 这些状态码会触发重试
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# 全局session
session = create_session()

def clean_wechat_article(url: str, output_txt: str = "article.txt", retry_count: int = 3) -> str:
    """
    爬取微信公众号文章内容
    
    Args:
        url: 文章链接
        output_txt: 输出文件名（注意：多个文章会覆盖，建议不使用）
        retry_count: 重试次数
    
    Returns:
        文章文本内容，失败返回空字符串
    """
    # 更完整的请求头，模拟真实浏览器
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Cache-Control": "max-age=0",
        "Referer": "https://mp.weixin.qq.com/"
    }
    
    for attempt in range(retry_count):
        try:
            # 使用session发送请求（自动重试）
            response = session.get(url, headers=headers, timeout=20, allow_redirects=True)
            
            # 检查响应状态码
            if response.status_code != 200:
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                    continue
                print(f"[跳过] HTTP状态码错误 {response.status_code}：{url}")
                return ""
            
            # 检查响应内容是否为空
            if not response.text or len(response.text) < 100:
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)
                    continue
                print(f"[跳过] 响应内容为空或过短：{url}")
                return ""
            
            soup = BeautifulSoup(response.text, "lxml")
            
            # 尝试多种方式查找正文区域
            content_div = soup.find("div", id="js_content")
            
            # 如果找不到，尝试其他可能的标签
            if not content_div:
                # 尝试查找包含文章内容的div
                content_div = soup.find("div", class_=re.compile("rich_media_content|js_content"))
            
            if not content_div:
                # 检查是否是文章已删除的情况
                deleted_keywords = ["该内容已被发布者删除", "内容已被删除", "文章已删除", 
                                    "此内容因违规", "该内容无法查看", "内容不存在", 
                                    "该内容已被删除", "此内容不存在"]
                if any(keyword in response.text for keyword in deleted_keywords):
                    print(f"[跳过] 文章已删除：{url}")
                    return ""
                
                # 检查是否被反爬虫拦截（通常会有特定提示）
                if "验证" in response.text or "安全验证" in response.text or "captcha" in response.text.lower():
                    print(f"[跳过] 可能触发反爬虫验证：{url}")
                    return ""
                
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)
                    continue
                print(f"[跳过] 未找到正文区域：{url}")
                return ""
            
            # 删除不需要的标签
            for tag in content_div(["script", "style", "svg", "img", "figure", "iframe", "video", "audio"]):
                tag.decompose()
            
            # 提取文本
            text = content_div.get_text(separator="\n")
            text = re.sub(r"\n{2,}", "\n", text.strip())
            
            # 检查是否是文章已删除的提示（在提取的文本中检查）
            deleted_keywords = ["该内容已被发布者删除", "内容已被删除", "文章已删除", 
                                "此内容因违规", "该内容无法查看", "内容不存在", 
                                "该内容已被删除", "此内容不存在"]
            if any(keyword in text for keyword in deleted_keywords):
                print(f"[跳过] 文章已删除：{url}")
                return ""
            
            # 检查提取的文本是否为空
            if not text or len(text.strip()) < 10:
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)
                    continue
                print(f"[跳过] 提取的文本为空或过短：{url}")
                return ""
            
            # 只在第一次成功时写入文件（避免覆盖）
            if attempt == 0:
                with open(output_txt, "w", encoding="utf-8") as f:
                    f.write(text)
            
            return text
            
        except requests.exceptions.Timeout:
            if attempt < retry_count - 1:
                print(f"[重试 {attempt + 1}/{retry_count}] 请求超时：{url}")
                time.sleep(2 ** attempt)
                continue
            print(f"[跳过] 请求超时（已重试{retry_count}次）：{url}")
            return ""
            
        except requests.exceptions.RequestException as e:
            if attempt < retry_count - 1:
                print(f"[重试 {attempt + 1}/{retry_count}] 网络错误：{url} —— {e}")
                time.sleep(2 ** attempt)
                continue
            print(f"[跳过] 网络请求失败：{url} —— {e}")
            return ""
            
        except Exception as e:
            if attempt < retry_count - 1:
                print(f"[重试 {attempt + 1}/{retry_count}] 处理错误：{url} —— {e}")
                time.sleep(2 ** attempt)
                continue
            print(f"[跳过] 处理失败：{url} —— {e}")
            return ""
    
    return ""


# if __name__ == "__main__":
    # article = clean_wechat_article(URL)
    # print(clean_wechat_article(URL))          # 终端打印

wxarticles = []
failed_urls = []  # 记录失败的URL

for i in tqdm(wxurl, desc="从链接提取微信文章"):
    result = clean_wechat_article(i)
    wxarticles.append(result)
    
    # 记录失败的URL
    if not result:
        failed_urls.append(i)
    
    # 添加请求间隔，避免触发限流（每2-3个请求间隔1-2秒）
    if len(wxarticles) % 3 == 0:
        time.sleep(1)  # 每3个请求后休息1秒 
    else:
        time.sleep(0.3)  # 其他请求间隔0.3秒

# 输出统计信息
success_count = sum(1 for article in wxarticles if article)
print(f"\n[统计] 成功：{success_count}/{len(wxurl)}，失败：{len(failed_urls)}/{len(wxurl)}")

# 如果有失败的URL，输出它们
if failed_urls:
    print(f"\n[失败链接] 共{len(failed_urls)}个：")
    for url in failed_urls:
        print(f"  - {url}")



