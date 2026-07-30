from b站热搜 import print_bilihot
from 获取b站up更新情况 import print_up_video
from 爬取wx公众号文章信息 import print_wxoa
from kkgithub热榜 import print_kkgithub
# 记录-->6月12日创业邦哔哩哔哩空间地址：https://space.bilibili.com/405261267    (+?spm_id_from=333.337.search-card.all.click)
# 记录-->6月12日周鸿祎哔哩哔哩空间地址：https://space.bilibili.com/627947058    (+?spm_id_from=333.337.search-card.all.click)

# token：1413576726
#################微信公众号网站（供传入print_wxoa()）
# 1.机器之心
机器之心 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzA3MzI4MjgzMw==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1413576726&lang=zh_CN&f=json&ajax=1"
# 2.量子位
量子位 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzIzNjc1NzUzMw%3D%3D&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1413576726&lang=zh_CN&f=json&ajax=1"
# 3.创业邦
创业邦 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5OTAzMjc4MA==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1413576726&lang=zh_CN&f=json&ajax=1"
# 4.新智元
新智元 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzI3MTA0MTk1MA==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1413576726&lang=zh_CN&f=json&ajax=1"
# 5.XR Vision Pro
xrvision = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5OTY1ODgxMg==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1413576726&lang=zh_CN&f=json&ajax=1"
# 6.阿里云开发者
阿里云开发者 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5OTY1ODgxMg==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1413576726&lang=zh_CN&f=json&ajax=1"
# 7.APPSO
appso = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5MjAyNDUyMA==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1413576726&lang=zh_CN&f=json&ajax=1"
# 8._36氪
_36氪 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzI2NDk5NzA0Mw==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1413576726&lang=zh_CN&f=json&ajax=1"
# 9.CodeSheep
codesheep = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzU4ODI1MjA3NQ==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1413576726&lang=zh_CN&f=json&ajax=1"
# 10.智能涌现
智能涌现 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzkwMDQ2NDU2Nw==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=1413576726&lang=zh_CN&f=json&ajax=1"


榜单 = "11" # 榜单[0]和榜单[1]取值分别代表是否输出b站热搜和github热榜，“0”代表不输出，“1”代表输出
if 榜单[0] == "1":
    print_bilihot()
if 榜单[1] == "1":
    print_kkgithub()

work = "00" # work[0]和work[1]取值分别代表是否输出常更新和少更新的up主视频，公众号信息，“0”代表不输出，“1”代表输出
play = "00" #同变量work
if work[0] == "1":
    
    print("####################### b站 metagpt 视频#######################")
    print_up_video("metagpt")
    print("####################### b站 周鸿祎 视频#######################")
    print_up_video("周鸿祎")
    print("####################### b站 创业邦 视频#######################")
    print_up_video("创业邦")
    print("####################### wxoa 量子位 #######################")
    print_wxoa(量子位)
#    print("####################### wxoa 新智元 #######################")


if work[1] == "1":
    print("####################### b站 秋芝2046 视频#######################")
    print_up_video("秋芝2046")
    print("####################### b站 同济子豪兄 视频#######################")
    print_up_video("同济子豪兄")
    print("####################### b站 AI研究室-帆哥 视频#######################")
    print_up_video("AI研究室-帆哥")
    print("####################### b站 无处安放的小A 视频#######################")
    print_up_video("创业邦")
    print("####################### b站 小Lin说 视频#######################")
    print_up_video("小Lin说")
    print("####################### b站 ai产品观察 视频#######################")
    print_up_video("ai产品观察")
    print("####################### b站 metagpt 视频#######################")
    print_up_video("metagpt")





if play[0] == "1":
    print("####################### b站 柳冲冲 视频#######################")
    print_up_video("柳冲冲")
    print("####################### b站 我不是黄毛 视频#######################")
    print_up_video("我不是黄毛")    
 

if play[1] == "1":
    print("####################### b站 henry的小木屋 视频#######################")
    print_up_video("henry的小木屋")
    print("####################### b站 毕的二阶导 视频#######################")
    print_up_video("毕的二阶导")    

