# Python编写一个简单的密码爆破工具

**此次实验有一下环境要求：**
- 需要python3.9+版本
- 密码来自于CentOS7
- 准备一个弱密码字典
- 不可以在windows环境下使用该代码(因为crypt模块不支持windows系统下运行)

### 获取到靶机中的root密码的密文(在/etc/shadow中)
![image](https://github.com/hecker-zz/blog/assets/153266742/4bdee935-9ca3-4065-8d3e-d789f0add699)

### 以":"来切片密文，选取密码字段，也就是切片列表的第二个，获取的结果如下：
![image](https://github.com/hecker-zz/blog/assets/153266742/d7230c54-9ba2-44c3-8a5b-447f2b41694b)

### 获取盐值：就是第从开头到最后一个$符号的内容
![image](https://github.com/hecker-zz/blog/assets/153266742/ba6e7e8d-d5e9-4808-bbfd-13808bb7a45c)

### 将字典中的数据和获取到的盐值进行加密，之后进行密码爆破
![image](https://github.com/hecker-zz/blog/assets/153266742/822d2e1c-b8cc-4941-8b24-680d3bde5506)

### 使用kali进行爆破
![image](https://github.com/hecker-zz/blog/assets/153266742/716aac4c-d30c-4f60-9b60-61cb45de34a7)



### 源码:
```python
import crypt

#Centos7系统下的root账户的密文
key="root:$6$LcLi.DjLU/cE1tuW$8IV/jxsfqwvd7tgJLCCs2RI.MEyA3V85RtyO3BAxueXH3NBGOUEBZsICVddIV963fysaA.YFYVieUKpI69XjZ1::0:99999:7:::"

#字典的路径
dic="/tmp/dic.txt"

#以":"来切片密文，选取密码字段，也就是切片列表的第二个
cipher=key.split(":")[1]

#获取盐值就是第从开头到最后一个$符号的内容
salt=cipher[0:cipher.rfind("$")]
print(salt)

#将字典中的数据和获取到的盐值进行加密，之后进行密码爆破
with open(f"{dic}","r") as f:
    for password in f:
        password=password.strip()   #去除两端空白字符
        if crypt.crypt(password,salt)==cipher:
            print(password)

```