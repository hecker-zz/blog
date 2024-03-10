# 【漏洞复现】metinfo_5.0.4任意文件包含漏洞
- 任意文件包含就是一个文件中包含另一个文件，但是这个包含可以执行所包含文件的代码。
- 一般包含方式如：`include `、`include_once`、`require`、`require_once`等
- 可以使用动态包含，把文件名设为一个变量
- 该漏洞可以无视拓展名，直接读取(图片木马的执行)。能够无条件解析PHP代码
- 本次实验演示metinfo_5.0.4版本的文件包含漏洞。
### 这个漏洞只能在代码审计里发现，那么直接来到`MetInfo5.0.4\about\index.php`中，观察其代码包含了另一个文件`MetInfo5.0.4/include/module.php`和一个变量`$module`
![image](https://github.com/hecker-zz/blog/assets/153266742/20b8c062-777e-4969-a45a-c04b78de4f44)
### 直接去`MetInfo5.0.4/include/module.php`中又发现它也包含了一个文件`common.inc.php`，并且对mudule.php进行代码审计后发现，当fmodule这个变量不等于7时，它就会对$module进行验证。
![image](https://github.com/hecker-zz/blog/assets/153266742/45cebd16-babc-402f-ac1d-e7eb0c95dfb2)
![image](https://github.com/hecker-zz/blog/assets/153266742/40ce1852-4443-4f3d-b3a6-63b606410221)

### 来到`common.inc.ph`后进行代码审计，发现该处有漏洞的可能。
![image](https://github.com/hecker-zz/blog/assets/153266742/1cb109fa-6234-4064-b206-80847193b989)

### 直接来到metinfo的首页进行尝试，令fmodule=7并且module=c:/windows/system32/drivers/etc/hosts  ，让他去查看一下hosts文件。
![image](https://github.com/hecker-zz/blog/assets/153266742/639880d4-fe53-4cd1-b1c4-2ecfad589ef5)
### 发现能够成功执行，这样的话直接上传一个图片码，那么他就会执行。那就可以直连了。
###  图片马：
![image](https://github.com/hecker-zz/blog/assets/153266742/b9c9e047-9392-4cd6-94c7-d142e990f0e6)


###  图片马执行，看到了phpinfo()就代表图片马执行成功
![image](https://github.com/hecker-zz/blog/assets/153266742/7adf5f0d-9244-4fc0-a81c-6d6d89bda31f)


### 接下来就是蚁剑直连
![image](https://github.com/hecker-zz/blog/assets/153266742/0c8cde06-c68a-40db-95f4-de7c64354959)

### 拿到shell
![image](https://github.com/hecker-zz/blog/assets/153266742/4a2d9aee-d05b-4587-bb2f-d3b1e099f340)