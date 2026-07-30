import re
import requests
from bs4 import BeautifulSoup

# URL = "https://mp.weixin.qq.com/s/JQZpNgaFoivwR9fL_k-Aow"

def clean_wechat_article(url: str, output_txt: str = "article.txt") -> str:
    """抓取公众号文章正文，返回并保存为纯文本"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    html = requests.get(url, headers=headers, timeout=15).text
    soup = BeautifulSoup(html, "lxml")

    # 公众号正文都在 id="js_content" 的 div 里
    content_div = soup.find("div", id="js_content")
    if not content_div:
        raise RuntimeError("未找到正文区域，请检查链接是否有效")

    # 删掉脚本、样式、svg、图片、二维码等
    for tag in content_div(["script", "style", "svg", "img", "figure"]):
        tag.decompose()

    # 拿纯文本
    text = content_div.get_text(separator="\n")

    # 去掉空白行、首尾空格、多余空行
    text = re.sub(r"\n{2,}", "\n", text.strip())



    return text


if __name__ == "__main__":
    # article = clean_wechat_article(URL)
    # print(clean_wechat_article(URL))          # 终端打印
####################### wxoa 量子位 #######################
    print(clean_wechat_article("https://mp.weixin.qq.com/s/u1p9Gu78NJeIM7XgB2pGxg"))

