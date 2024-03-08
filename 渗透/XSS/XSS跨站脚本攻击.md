# XSS就是跨站脚本攻击(Cross Site Scripting)按理来说应该叫CSS的，但是CSS比他出来的早，名字被用过了，所以就叫XSS了。
- 就是主要利用Javascript来进行恶意攻击。
- 实验环境是cms
### 首先尝试一下反射型XSS，这种攻击类型的不持久，只有在特定条件下触发。首先利用搜索框来注入一个弹窗的XSS
```java
<script>alert(/我是XSS!!/)</script>
```
- 把上方代码放入搜索框中就会出现这样的效果：
![image](https://github.com/hecker-zz/blog/assets/153266742/4998a75f-f452-41f3-be11-bcd1566c3272)

### 还有存储型的XSS，这种一般写留言板中，他会把数据存储在服务端，一旦有人打开留言板就会收到攻击，包括管理员审核该条留言.
![image](https://github.com/hecker-zz/blog/assets/153266742/2a17d14e-6f89-4644-93c1-547fb3ad70c8)

### DOM型的XSS是修改受害者浏览器页面的DOM来执行的。
- 这次主要是为了能看到直观的效果所以直接弹窗，实际的XSS攻击往往是悄无声息的。
- 而且XSS的攻击千变万化，会衍生出很多变形的XSS代码。例如：
```javascript
<ScRiPt>alert(/我是XSS！！/)</ScRiPt>  //大小写转换
<Scr<Script>ipt>alert(/我是XSS/)</Scr</Script>ipt>  //关键字双写
//伪协议转码(就是把script转为ASCII码再整体URL编码)
//折分跨站
//还可以结合CSRF进行攻击
//...

```