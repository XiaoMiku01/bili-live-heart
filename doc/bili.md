# B站Cookie获取教程  
## 第一步：
打开你所用浏览器的**无痕模式**
- Microsoft Edge 浏览器  
右上角：`新建 InPrivate 窗口`  
![新建 InPrivate 窗口](http://i0.hdslb.com/bfs/album/dc2f069dd147ac2ade026a2be28294a69aebcd38.png)  
- Google Chrome 浏览器  
右上角：`打开新的无痕式窗口`  
![打开新的无痕式窗口](http://i0.hdslb.com/bfs/album/1e83b939af5d7ef4c08d11060e66bb5c1cf1bd27.png)  
- 其他浏览器  
略  
## 第二步：  
- 在**无痕窗口**进入任意一个直播间  
- 在直播间页面点击右上角登录自己的B站账号  
## 第三步：  
- 点击键盘`F12`或者`鼠标右键`->检查，进入开发者工具  
- 点击`网络`/`NetWork`选项卡  
![网络/Network](http://i0.hdslb.com/bfs/album/4717448339d26a412ba23215d3ce674c549adf4f.png)  
- 进入该选项卡后，键盘`F5`或浏览器左上角刷新页面  
- 在数据包中找到**heartBeat**或**webHeartBeat**，点击找到请求头中的**cookie**项，并复制保留（图中浅蓝色部分）后面部署会用到这个cookie  
![cookie](http://i0.hdslb.com/bfs/album/01c052ec17757a34f6a256f03523efa89c3e4d56.jpg)  
PS:有了cookie能操作B站账号的大部分功能，切勿泄露或分享出去
## 如果后续打卡出现KeyError('LIVE_BUVID',)报错,请关闭无痕模式抓cookie
