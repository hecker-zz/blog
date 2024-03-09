# SQL注入(联合查询)拿下CMS

- 靶场环境选择cms
- 靶机IP:192.168.200.148

### 进入靶场环境找找看有没有可以sql注入的地方，url中进行尝试使用字符和注释的手段查看页面是否报错






### 经过测试发现新闻界面可能存在数字型sql注入，因为可以通过url中id号的加减法运算得到页面。由此证明传的是数字型参数。
![image](https://github.com/hecker-zz/blog/assets/153266742/49ae304a-7671-4745-86fd-d21861e8a7d1)






### 对该情况尝试使用ORDER BY 语句排序试试，发现能够执行SQL语句，证明该处存在sql注入漏洞。
![image](https://github.com/hecker-zz/blog/assets/153266742/c617ea91-5679-446f-82c4-6f09cf8d0577)






### 发现可以执行且有第五列，继续使用ORDER BY 语句测试后发现使用15能够执行，16的时候报错了，由此证明共有15列.
![image](https://github.com/hecker-zz/blog/assets/153266742/4f757b19-f17f-4acb-8ae2-451a7370d15e)





### 直接把前面给弄成false，并且用联合查询发现能够显示的列数只有3和11列
![image](https://github.com/hecker-zz/blog/assets/153266742/7ee0bf09-356b-4259-8369-62f0b34dcdb7)





### 利用3和11查看数据库的版本和数据库名分别是mysql5.5和cms
![image](https://github.com/hecker-zz/blog/assets/153266742/ca4a3d9c-541a-4a71-9d00-d9eef9028fbd)





### 知道了数据库名接下来利用mysql默认的数据库information_schema来查询cms数据库下的表 （注意:因为直接查询的话会只显示第一个表名，但是我们需要的是列出所有表名，所以用group_concat()来包裹它的列名，另外发现直接传字符串过去会报错，说只支持数字型，所以用hex()把group_concat()的内容再包住，就是把数据转为16进制）
![image](https://github.com/hecker-zz/blog/assets/153266742/68199520-115e-4f28-b0ea-a84437358937)





### 发现是十六进制的字符串，那么直接拿去转码。如此一来我们就拿到了cms数据库中的所有表名，观察发现cms_users是我们需要的表
![image](https://github.com/hecker-zz/blog/assets/153266742/b2727957-d900-4125-af3b-041a456f6ee0)




### 有了表名我们直接查询有哪些列（注:表名一定要用引号套起来，不然你可能会头疼、抑郁、甚至死亡）
![image](https://github.com/hecker-zz/blog/assets/153266742/19ce829e-d40d-4316-b4d9-08b9f8271284)



### 拿到直接转码发现username和password这俩列名，那么思路一下就清晰了。
![image](https://github.com/hecker-zz/blog/assets/153266742/f03c5376-6a81-4043-a5fc-5cb1dbc2067e)



### 知道了表名，列名，数据库名，那么直接查询即可,查完直接转码!
![image](https://github.com/hecker-zz/blog/assets/153266742/deea3e3a-6d5f-40f8-affa-52ea31683bfb)





![image](https://github.com/hecker-zz/blog/assets/153266742/f38e8eed-9a13-4b25-9d17-709c270b50e5)



### 后面这串东西肯定是加密了的，一看32位，盲猜md5，直接转码去咯
![image](https://github.com/hecker-zz/blog/assets/153266742/c8c92ab1-ace4-4cc7-966b-f7615107f55d)


### 有了账号密码去登录验证一下，发现成功登录管理界面！
![image](https://github.com/hecker-zz/blog/assets/153266742/48fc3b45-ae8a-4684-afc6-3ca17ac52c18)