from llm总结文章list import list_idx 
from 获取解释词语的位置 import 需解释词语位置
from tqdm import tqdm
list_marked03 = []
list_unmarked03 = []

# 将list_idx转换为集合，使查找操作的时间复杂度从O(n)降至O(1)
list_idx_set = set(list_idx)

# list_marked03: 带标记词语位置的列表，list_unmarked03: 不带标记词语位置的列表
for i in tqdm(range(len(需解释词语位置)), desc="分割词语位置列表"):
    if i in list_idx_set:
        list_marked03.append(需解释词语位置[i])
    else:
        list_unmarked03.append(需解释词语位置[i])


# print(f"list_marked03: {list_marked03}")
# print(f"list_unmarked03: {list_unmarked03}")