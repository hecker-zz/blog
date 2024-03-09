# Python编写爬取网站图片的脚本

- 导入re和requests两个模块

### 获取需要爬取网站的url，这里以我靶机为例
![image](https://github.com/hecker-zz/blog/assets/153266742/3e002c7f-1c9b-446d-b030-a06968ee752a)


### 定义一个函数用get拿到网页的源码
![image](https://github.com/hecker-zz/blog/assets/153266742/e8303cde-3a72-424b-a972-f6a6a05446b7)

### 再定义一个函数用来获取图片列表(通过观察可以发现靶机网站的图片都是以style/开头，以.jpg结尾。)
![image](https://github.com/hecker-zz/blog/assets/153266742/29012ccd-0e68-4d9e-9c28-806388f155fc)


### 直接把上述两个地址拼接一下就可以得到完整的图片url了，我们直接建一个循环把列表中图片挨个取出存到本地即可
![image](https://github.com/hecker-zz/blog/assets/153266742/0beafef8-c668-4a43-b320-d8f822d792b4)


### 查看代码运行结果
![image](https://github.com/hecker-zz/blog/assets/153266742/f5a3cc03-6bc0-448a-8072-68ff785abf66)




### 源码：

```python

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
```