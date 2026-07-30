from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import re
# from kkgithub热榜 import ghname, ghdescri  # 假设这两个变量在你的爬虫文件中
# from b站热搜 import bseartitle
# from 爬取wx公众号文章信息 import wxtim, wxurl, wxtitle
# from 获取b站up更新情况 import bupdate, buptitle
from llm总结文章list import list_marked01,list_unmarked01
from 分割文章链接列表 import list_marked02,list_unmarked02
from 分割词语位置列表 import list_marked03,list_unmarked03
from github热榜 import fetch_github_trending
from 爬取producthunt热榜 import fetch_producthunt_data

app = FastAPI()

# 允许所有来源跨域（生产环境建议限制）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/api/ghname")
# def get_ghname():
#     return ghname
# @app.get("/api/ghdescri")
# def get_ghdescri():
#     return ghdescri
# @app.get("/api/bseartitle")
# def get_bseartitle():
#     return bseartitle
# @app.get("/api/wxtim")
# def get_wxtim():
#     return wxtim
# @app.get("/api/wxurl")
# def get_wxurl():
#     return wxurl
# @app.get("/api/wxtitle")
# def get_wxtitle():
#     return wxtitle
# @app.get("/api/bupdate")
# def get_bupdate():
#     return bupdate
# @app.get("/api/buptitle")
# def get_buptitle():
#     return buptitle


####### 以下为公众号文章总结和词语位置（包含重点和非重点） #######
@app.get("/api/summary01")
def get_summary01():
    return list_marked01
@app.get("/api/wordposition01")
def get_wordposition01():
    return list_marked03
@app.get("/api/url01")
def get_url01():
    return list_marked02
@app.get("/api/url02")
def get_url02():
    return list_unmarked02
@app.get("/api/summary02")
def get_summary02():
    return list_unmarked01
# @app.get("/api/wordposition02")
# def get_wordposition02():
#     return list_unmarked03

####### 以下为producthunt热榜 #######
@app.get("/api/producthunt")
def get_producthunt():
    display_ph, _ = fetch_producthunt_data()
    return display_ph

@app.get("/api/producthunt_urls")
def get_producthunt_urls():
    _, display_phurls = fetch_producthunt_data()
    return display_phurls

####### 以下为github热榜相关信息 #######
@app.get("/api/github")
def get_github():
    display_gh, _ = fetch_github_trending()
    return display_gh

@app.get("/api/github_name")
def get_github_name():
    _, ghname = fetch_github_trending()
    return ghname

####### 以下为写入文件接口 #######
class TextList(BaseModel):
    texts: List[str]

def write_texts_to_file_helper(file_path: str, texts: List[str], item_label: str = "文章"):
    """写入文本到文件的辅助函数"""
    try:
        # 以追加模式打开文件，使用UTF-8编码
        with open(file_path, 'a', encoding='utf-8') as f:
            # 写入分隔线和时间戳
            from datetime import datetime
            f.write(f"\n\n\n\n写入时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # 写入所有文本，每条文本之间用空行分隔
            for text in texts:
                # 去掉开头的标号（如'12.'、'5.'等），只去掉第一个匹配项
                text = re.sub(r'^\d+\.', '', text, count=1)
                f.write(text)
                f.write("\n")
        
        return {"status": "success", "message": f"成功写入 {len(texts)} 条文本到文件", "file_path": file_path}
    except Exception as e:
        return {"status": "error", "message": f"写入文件失败: {str(e)}"}

@app.post("/api/write_texts_to_file")
def write_texts_to_file(text_list: TextList):
    file_path = '/home/bill/桌面/公众号文章整理.txt'
    return write_texts_to_file_helper(file_path, text_list.texts, "文章")

@app.post("/api/write_texts_to_github_file")
def write_texts_to_github_file(text_list: TextList):
    file_path = '/home/bill/桌面/github项目整理.txt'
    return write_texts_to_file_helper(file_path, text_list.texts, "项目")

@app.post("/api/write_texts_to_producthunt_file")
def write_texts_to_producthunt_file(text_list: TextList):
    file_path = '/home/bill/桌面/producthunt产品整理.txt'
    return write_texts_to_file_helper(file_path, text_list.texts, "产品")


