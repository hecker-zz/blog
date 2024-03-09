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

