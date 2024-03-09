# Python编写一个简单的内网主机存活检测工具

- 需要安装scapy模块，主要用来发送、捕获、分析网络数据包(win系统:  pip install scapy)
- ICMP报文type含义为    0:应答 3:目标不可达 5:重定向  8:响应

### 上来直接导入scapy和logging模块，再关闭告警(不关闭的话会很乱)
![image](https://github.com/hecker-zz/blog/assets/153266742/94ed639a-ef42-4428-a55f-623e91f8d987)



### 向内网中的每个主机发送一个ICMP数据包，如果收到响应就代表着主机存活
![image](https://github.com/hecker-zz/blog/assets/153266742/985f8d6c-2f69-4ff7-b2b7-1f82029d2aca)


### 测试实验结果：
![image](https://github.com/hecker-zz/blog/assets/153266742/7cc653d5-8d39-406c-8f2f-3404c804f1dd)


### 源码:
```python

from scapy.all import *
import logging
#关闭告警
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

src="192.168.200.148"
for i in range(1,255):
    dst=f"192.168.200.{i}"
    print(f"\r[-] scaning for {dst}",end="")
    pkt=IP(src=src,dst=dst)/ICMP()

    #发送请求，设置等待时间0.2s，且不显示详细信息
    res=sr1(pkt,timeout=0.2,verbose=False)  

    #请求的Type如果为0:应答 3:目标不可达 5:重定向  8:响应
    if res and res.type==0:  
        print(f"\n[+] {dst} is live!")

    
```