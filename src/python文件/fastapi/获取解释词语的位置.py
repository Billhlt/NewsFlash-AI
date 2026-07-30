from tqdm import tqdm
from 提取需解释的词语 import 需解释词语列表
from llm总结文章list import 总结内容list

bb = 总结内容list
aa = 需解释词语列表

# 核心算法
需解释词语位置 = []
for i in tqdm(range(len(aa)), desc="获取需解释位置进度"):
    j=i
    result = []
    # print(bb[j])
    for bkwd in aa[i]:
        # print(bkwd)
        if bkwd in bb[j]:  # 先检查关键词是否在文本中
            result.append([bb[j].index(bkwd), bb[j].index(bkwd) + len(bkwd)])
        else:
            print("##############################未找到关键词："+bkwd+"##############################")  # 如果找不到，用-1表示
    需解释词语位置.append(result)
# print(需解释词语位置)
# print(需解释词语位置列表)
# 现在 optimized_articles 就是优化后的字符串列表
# for art in optimized_articles:
#     print(art, "\n" + "-"*40)