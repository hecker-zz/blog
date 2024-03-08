import requests
import re


#网页url
url="http://192.168.200.148/pythonSpider/"


#获取网页源码
def get_content(url):
    res=requests.get(url=url)
    return res.text


#获取图片的路径
html=get_content(url)
def imgs_list(html):
    img_list=re.findall(r"style/\w+\.jpg",html)
    return img_list




#下载图片到本地,content就是以二进制打开。
for i in range(0,len(imgs_list(html))):
    img_path=url+imgs_list(html)[i]
    res=requests.get(img_path)
    with open(f"./images/{i}.jpg","wb") as f:
        f.write(res.content)
        print(img_path)
