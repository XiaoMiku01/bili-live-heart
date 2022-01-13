# 腾讯云函数部署

::: tip 提示
此方式目前完全免费！部署前请确保已经获取到[**B站cookie**](/Guide/Cookie)和[**SendKey**](/Guide/SendKey)  
**云函数版暂不支持一个函数多个账号，如有需要可以自己新建函数（反正不要钱~~）**  
**来的小可爱记得认真看哦**  
:::

## 1.1 下载云函数压缩包(二选一)
记得下载最新版哦~
- [Github](https://github.com/XiaoMiku01/bili-live-heart/releases/)
- [百度云](https://pan.baidu.com/s/1CR4G6_59zzhASPwZR5wZcQ?pwd=soul) 提取码：soul  

## 1.2 部署代码上云
- 登录[腾讯云函数官网](https://cloud.tencent.com/product/scf) 并进入控制台  
![image_1641823475372.png](https://s2.loli.net/2022/01/10/wo9QNOkLdA243DG.png)
::: tip 提示
微信小程序「腾讯云助手」也可以进行以下操作，搜索云产品：云函数，即可
:::
- 选择函数服务 - 新建  
![image_1641823807969.png](https://s2.loli.net/2022/01/10/aKD7En2ZugewhzV.png)  

- 选择自定义创建 - 事件函数-函数名称随意-地域国内随意 - 代码部署 - 运行环境选择Python3.6  
![image_1641823844125.png](https://s2.loli.net/2022/01/10/4ypeOKRalcLPTrW.png)  

- 提交方法选择本地上传zip包 - 执行方法**默认不要改** - 函数代码上传刚刚下载的压缩包  
![image_1641823880776.png](https://s2.loli.net/2022/01/10/CNfU2OjkGDWSbKP.png) 

- 点开高级配置 - 环境配置  

先到下面把**异步执行**打钩,再回到上面填执行超时时间填86400
环境变量填写自己[B站cookie](/Guide/Cookie)，需要赠送小心心的主播uid(ruid，不填则只进行签到不赠送小心心**只能填一个**)，Server酱的[SendKey](/Guide/SendKey)  
::: tip 提示
弹幕打卡的不需要填写，会自动打卡  
**key栏中的字母全为小写 右边一栏才是你填的**
:::  

![image_1641824927711.png](https://s2.loli.net/2022/01/10/nVmWzYlE9bTUhiM.png)  

- 其他配置不变 - 展开触发器配置  
选择自定义创建 - 触发方式：定时触发 - 触发周期：每一天
::: tip 提示
也可以自己写Cron表达式,自定义时间运行,例如下图表示每天0点30运行：
![image_1641825271870.png](https://s2.loli.net/2022/01/10/wslNVLMHaYgFbjR.png)  
补充：五位数Cron表达式，第一位表示分，第二位表示时，后三位本项目用不到不解释，例如：  
`10 0 * * *` 表示每天0点10分运行  
`30 8 * * *` 表示每天8点30分运行  
`50 20 * * *` 表示每天20点50分运行  
:::
- 点击**完成**
- 等创建成功后点击**立即转跳**
- 点击左边的函数管理 - 函数代码 - 左下角 - 测试  

![image_1641824304907.png](https://s2.loli.net/2022/01/10/s8NR3jyL5JZvkBr.png)  

![image_1641824349083.png](https://s2.loli.net/2022/01/10/gFWaXhDnkLdSqTG.png)  

- 耐心等待10-15分钟，查看返回日志是否运行成功  
![image.png](https://s2.loli.net/2022/01/10/AxuQC5rjG1v3kZO.png)  
::: tip 提示
如果你设置了Server酱推送，测试完也会收到推送消息哦~
:::

## 1.3如何升级云函数？  
- 下载新版压缩包  
- [Github](https://github.com/XiaoMiku01/bili-live-heart/releases/)
- [百度云](https://pan.baidu.com/s/1CR4G6_59zzhASPwZR5wZcQ?pwd=soul) 提取码：soul   

- 进入创建的函数，选择函数代码，选择本地上传zip包  
![image_1642090877940.png](https://s2.loli.net/2022/01/14/u1oMOR2CgqlcWA7.png)  

- 点击部署即可，然后就可以测试了，无需重新配置函数和环境变量