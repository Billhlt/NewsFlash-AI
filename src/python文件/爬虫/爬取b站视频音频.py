import requests
import re # 正则表达式模块
import json
url = "https://www.bilibili.com/video/BV1tMEAzJEXi?spm_id_from=333.788.playrecommendByOp.0&vd_source=19885d73461009f3d8594b8491f48690"
headers = {    
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
   ,"Referer": "https://www.bilibili.com/"
}

response = requests.get(url, headers=headers)
# print(response.text)
data = response.text
# window.__playinfo__=(.*?)</script> # ()为正则表达式中的捕获组，.*?为非贪婪匹配，即尽可能少的匹配字符，</script>为结束标志，*为匹配前面的字符0次或多次，？为非贪婪匹配，.为匹配除换行符以外的单个任意字符
playinfo = re.findall('window.__playinfo__=(.*?)</script>',data)[0] 
# 注释：re模块的findall()函数会返回一个列表，这里返回的是函数中data和前面一个字符匹配的(.*?)的内容,[0]代表返回列表第一个元素
json_data=json.loads(playinfo) # 将字符串转换为json格式(字典)
# video_data = json_data['data']['dash']['video'][0]['baseUrl'] 
audio_data = json_data['data']['dash']['audio'][0]['baseUrl']
# video_dat = requests.get(video_data, headers=headers).content #  获取视频数据的二进制文件
audio_dat = requests.get(audio_data, headers=headers).content #  获取音频数据的二进制文件
print(json_data)
# with open('video01.mp4', 'wb') as f: #  以二进制写模式打开一个名为'video01.mp4'的文件，w是写，b是二进制
#     f.write(video_dat) #  将视频数据的二进制文件写入文件
# with open('audio01.mp3', 'wb') as f: #  以二进制写模式打开一个名为'audio01.mp3'的文件
#     f.write(audio_dat) #  将音频数据的二进制文件写入文件
# print(json_data['data']['dash']['video'][0]['baseUrl'])
# print(json_data['data']['dash']['audio'][0]['baseUrl'])
# 备注
