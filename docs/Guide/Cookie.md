# 获取你的B站Cookie

::: tip 什么是Cookie？
Cookie，有时也用其复数形式 Cookies。类型为“小型文本文件”，是某些网站为了辨别用户身份，进行Session跟踪而储存在用户本地终端上的数据（通常经过加密），由用户客户端计算机暂时或永久保存的信息
<p align="right">——《百度百科》</p>
管他那么多，简单来说就是B站的 Cookie 和你的**账号密码**是等效的！
:::
:::warning 警告！
下面的方法获取的Cookie可能会不能用！请尝试用老方法获取！👉[如何获取B站Cookie](https://github.com/XiaoMiku01/bili-live-heart/blob/master/doc_old/bili.md) 尝试关闭或打开`浏览器无痕模式`，多试几次肯定能成功！
:::
## **打开B站任意一个直播间**  
这里当然选我然比的直播间了🥰👉[嘉然今天吃什么的直播间](https://live.bilibili.com/22637261)  
## **键盘`F12` 或者`鼠标右键`->检查，进入开发者工具**（以Edeg浏览器为例)  
![image_1641815150345.png](https://s2.loli.net/2022/01/10/hfGInjRDKsov5yE.png)  
## **选择`控制台`选项卡，输入以下代码，并回车确认**
```javascript
var cookie=document.cookie;
var ask=confirm(`点击确定复制你的Cookie`);
if(ask==true)
{copy(cookie);
msg=cookie}
```
![image_1641815561702.png](https://s2.loli.net/2022/01/10/6AjMucS4wEzpbe9.png)  
弹出提示框点`确定`，你的Cookie会自动复制到你的剪切板上，找个记事本粘贴上保留
![image_1641815634967.png](https://s2.loli.net/2022/01/10/xCgAaMYU6R4B8Xj.png)
:::warning 警告！
你的B站Cookie和你的账号密码是等效的，请勿轻易泄露你的Cookie!
:::