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

    