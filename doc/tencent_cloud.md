# 腾讯云函数部署教程（**推荐🌟**）
注意：此方法需要至少9个粉丝牌才能使用！若想要自动打卡送小心心则必须超过12个牌子  
## 第一步：  
下载云函数压缩包(二选一)  
- [Github](https://github.com/XiaoMiku01/bili-live-heart/releases/tag/zip)
- [百度云](https://pan.baidu.com/s/1cEWHDtfLaALCgpyzDK-DmQ) 提取码：asou  
## 第二步：
- 登录[腾讯云函数官网](https://cloud.tencent.com/product/scf) 并进入控制台  
![YZJ1896.png](http://i0.hdslb.com/bfs/album/6ad41c5f8a1d8fee0fab90a03d78f9e70c169d30.png@300h)  
- 选择函数服务 - 新建  
![XF~GC_UOPY_9SZM_L_F8D_1.png](http://i0.hdslb.com/bfs/album/52926f702b11afbafa9e25f621f1d5c7d078f0b0.png@300h)  
- 选择自定义创建 - 事件函数-函数名称随意-地域国内随意 - 代码部署 - 运行环境选择Python3.6  
![O_6_`TF02ZX1OFD5__Z@TJ7.png](http://i0.hdslb.com/bfs/album/f08676d18ea1b100cff49355809aa2cbcdeb2d22.png@300h)  
- 提交方法选择本地上传zip包 - 执行方法**默认不要改** - 函数代码上传刚刚下载的压缩包  
![_PU1N_1K539U_C~_EE85~PP.png](http://i0.hdslb.com/bfs/album/790491e7d5cabce4dbfcceb8e03d1794d42d0cdd.png@300h)  
- 点开高级配置 - 环境配置  
执行超时时间：**900**秒  
环境变量填写自己B站uid，B站cookie（[获取方式](bili.md)），需要赠送小心心的主播uid（ruid，如果为0或不填则只进行签到不赠送小心心），Server酱的[SendKey](https://sct.ftqq.com)（选填）  
（注意：**key栏中的字母全为小写**）  
![_DVA669_BPQ_BC~NSULLUDE.png](http://i0.hdslb.com/bfs/album/ff7eb9b5aa48d1564089a7c05c0df0a39368dd6a.png)
- 其他配置不变 - 展开触发器配置  
选择自定义创建 - 触发方式：定时触发 - 触发周期：每一天或自定义（自定义需要填写Cron表达式（[文档](https://cloud.tencent.com/document/product/583/9708#cron)）- 立即启用打钩✅ - 点击右下角完成  
![RO~8B_E5AE_A_24TYF5FI~U.png](http://i0.hdslb.com/bfs/album/3721468a778d1409b2fe504a295ab902a42fef93.png@300h)  
- 待创建成果后点击立即转跳 - 函数代码 - 左下角 - 测试  
![NQNA@W_LIV5X_~CEV_4EIVW.png](http://i0.hdslb.com/bfs/album/462a38540795117bd9d9a466a529c9de9593b2f6.png@300h)  

![FQ_I5F7@6JJSY_7RP8TNNM8.png](http://i0.hdslb.com/bfs/album/98c883eab94352e0af0103b060b68a2a5a6bc84a.png@300h)  

![6_UD_~MIY@DI30NI0_PO8VY.png](http://i0.hdslb.com/bfs/album/c3b546137d5a882b4074dd866fc80e1310dbbab5.png@300h)  

- 耐性等待10-15分钟，查看返回日志是否运行成功  
![~QCH3OAULJ_2U3_~@Y_7R8S.png](http://i0.hdslb.com/bfs/album/2ceb485547b8d6102a15cf948d58b6d5b182237a.png@300h)  
# 完
