# 腾讯云函数部署教程（**推荐🌟**）

## 第一步：  
下载云函数压缩包(二选一)  
- [Github](https://github.com/XiaoMiku01/bili-live-heart/releases/tag/0.8.0)
- [百度云](https://pan.baidu.com/s/1af5-r6Xpzmqmg44DQXW3xA) 提取码：soul  
## 第二步：
- 登录[腾讯云函数官网](https://cloud.tencent.com/product/scf) 并进入控制台  
![YZJ1896.png](http://i0.hdslb.com/bfs/album/6ad41c5f8a1d8fee0fab90a03d78f9e70c169d30.png@300h)  
- 选择函数服务 - 新建  
![XF~GC_UOPY_9SZM_L_F8D_1.png](http://i0.hdslb.com/bfs/album/52926f702b11afbafa9e25f621f1d5c7d078f0b0.png@300h)  
- 选择自定义创建 - 事件函数-函数名称随意-地域国内随意(最后不要选广州) - 代码部署 - 运行环境选择Python3.6  
![O_6_`TF02ZX1OFD5__Z@TJ7.png](http://i0.hdslb.com/bfs/album/f08676d18ea1b100cff49355809aa2cbcdeb2d22.png@300h)  
- 提交方法选择本地上传zip包 - 执行方法**默认不要改** - 函数代码上传刚刚下载的压缩包  
![_PU1N_1K539U_C~_EE85~PP.png](http://i0.hdslb.com/bfs/album/790491e7d5cabce4dbfcceb8e03d1794d42d0cdd.png@300h)  
- 点开高级配置 - 环境配置  
先到下面把**异步执行**打钩,再回到上面填时间，不少于7500  
环境变量填写自己B站uid，B站cookie（[获取方式](bili.md)），需要赠送小心心的主播uid（ruid，不填则只进行签到不赠送小心心**只能填一个**）弹幕打卡的不需要填写，会自动打卡，Server酱的[SendKey](https://sct.ftqq.com)（选填）  
（注意：**key栏中的字母全为小写 右边一栏才是你填的**）  
![_DVA669_BPQ_BC~NSULLUDE.png](https://b23.tv/JiN1ZY1
)
- 其他配置不变 - 展开触发器配置  
选择自定义创建 - 触发方式：定时触发 - 触发周期：每一天或自定义（自定义需要填写Cron表达式（[文档](https://cloud.tencent.com/document/product/583/9708#cron)）- 立即启用打钩✅ - 点击右下角完成  
常见Cron 表达式：  
每天中午12点运行：`0 0 12 */1 * * *`  
每天早上6点30运行：`0 30 6 */1 * * *`  
每天晚上8点运行：`0 0 20 */1 * * *`  
- 有时候运行一次无法获取满24个小心心，**请设置多个时间不同的触发器！！！两次触发器间隔最好大于2小时！**
![RO~8B_E5AE_A_24TYF5FI~U.png](http://i0.hdslb.com/bfs/album/3721468a778d1409b2fe504a295ab902a42fef93.png@300h)  
- 待创建成果后点击立即转跳 - 函数代码 - 左下角 - 测试  
![NQNA@W_LIV5X_~CEV_4EIVW.png](http://i0.hdslb.com/bfs/album/462a38540795117bd9d9a466a529c9de9593b2f6.png@300h)  

![FQ_I5F7@6JJSY_7RP8TNNM8.png](http://i0.hdslb.com/bfs/album/98c883eab94352e0af0103b060b68a2a5a6bc84a.png@300h)  

![6_UD_~MIY@DI30NI0_PO8VY.png](http://i0.hdslb.com/bfs/album/c3b546137d5a882b4074dd866fc80e1310dbbab5.png@300h)  

- 耐性等待10-15分钟，查看返回日志是否运行成功  
![~QCH3OAULJ_2U3_~@Y_7R8S.png](http://i0.hdslb.com/bfs/album/2ceb485547b8d6102a15cf948d58b6d5b182237a.png@300h)  

· 添加触发器  
![添加触发器](https://b23.tv/sxdXEEh)
# 完
