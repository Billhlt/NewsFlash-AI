from llm总结文章list import list_idx 
from 爬取wx公众号文章信息 import wxurl
from tqdm import tqdm

list_marked02 = []
list_unmarked02 = []

# 将list_idx转换为集合，使查找操作的时间复杂度从O(n)降至O(1)
list_idx_set = set(list_idx)

# list_marked02: 带标记的文章的链接列表，list_unmarked02: 不带标记的文章的链接列表
for i in tqdm(range(len(wxurl)), desc="分割文章链接列表" ):
    if i in list_idx_set:
        list_marked02.append(wxurl[i])
    else:
        list_unmarked02.append(wxurl[i])

# print(f"list_marked02: {list_marked02}")
# print(f"list_unmarked02: {list_unmarked02}")