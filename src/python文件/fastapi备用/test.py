from tqdm import tqdm
a=[]
b=[11,2,3,4,5,6,7,8,9,10,11,2,3,4,5,6,7,8,9,10,11,2,3,4,5,6,7,8,9,10]
for i in tqdm(b, desc="清洗文章"):
    a.append(i)
    
print(a)