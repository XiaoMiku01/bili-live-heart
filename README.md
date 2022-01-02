<div align="center">

# **Bilibili粉丝牌助手**  

 </div>

2022-1-2更新  v0.7.3

基于Python3异步开发的自动获取每日小心心及直播间自动打卡脚本  
运行环境：不低于Python3.6  
***  

## 已实现功能  
> 直播区每日签到 ✅  
> 每日获取24个小心心 ✅  
> 指定房间每日弹幕打卡并赠送小心心、辣条 ✅  
> Server酱微信推送 ✅  
> 自动弹幕打卡所有粉丝牌房间 ✅   
## 更新修复  
请大家及时更新代码，云函数版请删除先前创建的函数，重新下载压缩包部署  
> **2021**  
> 10-30 [0.2.0]修复：B站接口失效导致无法正常签到、送小心心  
> 11-1  [0.3.0]修复：Server酱推送失败问题，概率无法赠送所有小心心问题  
> 11-11 [0.4.0]修复：短房间号发送心跳、弹幕请求失败问题，当背包初始为空时程序会异常报错问题  
新增：自动赠送辣条、自动弹幕打卡所有粉丝牌房间、自动每日700银瓜子兑换1硬币、部署时ruid不填或为0时将不赠送礼物  
> 11-12 [0.5.0]修复：当粉丝牌主人未开通直播间会报错  
> 11-13 [0.6.0]修复：在特殊房间弹幕打卡失败问题  
> 12-7 [0.7.0] 修复好多bug!!!不列了，开摆！  
> 12-31 [0.7.1] ~~运行逻辑优化，Server酱推送优化~~ 此版本有严重bug，无法使用  
> **2022**  
> 1-1 [0.7.2] 修复：小心心获取&赠送异常、README.md中流程图错误，Server酱推送优化  
> 1-2 [0.7.3] 修复：B站接口问题导致的脚本失效，更改版本号避免混淆  
## 部署方式  
> ### 腾讯云函数版（**推荐🌟**）  
> >优点：  
免费、稳定、无需服务器、零基础部署  
缺点：  
~~由于腾讯云函数限制了最长15分钟运行时间，所以至少需要9个粉丝牌才能拿满24个小心心。同时如果要想运行后续签到，则必须要至少12个牌子，否则云函数会超时报错，但是任然会得到24个小心心~~  
>更新解决方案：创建函数时，把高级选项里的【异步执行】打开，然后回到上面【超时时间】填到最大，能突破15分钟；不过如果要是没有9个粉丝牌，就把index.py 第17行的 cloud_service=True 改成 cloud_service=False ([issue#17](https://github.com/XiaoMiku01/bili-live-heart/issues/17#issuecomment-1000831925))  

> ### 本地运行版  
> > 优点：  
没有粉丝牌数量限制  
缺点：  
需要自己搭建本地Python环境，设置定时任务  

## 详细教程  
- [获取B站Cookie](doc/bili.md)（**🌟这个很重要🌟**）  
- [Server酱推送](https://sct.ftqq.com/)（可选）  
- [腾讯云函数运行](doc/tencent_cloud.md) / [本地运行](doc/local.md)（二选一）  

## 常见问题   
- 获取小心心报错，如：用户不存在，KeyError('LIVE_BUVID',)，请重新抓取cookie！！  
- 每日小心心无法获取24个，请更换云函数的运行位置，或触发器运行时间 常见Cron 表达式：  
每天中午12点运行：`0 0 12 */1 * * *`  
每天早上6点30运行：`0 30 6 */1 * * *`  
每天晚上8点运行：`0 0 20 */1 * * *`  
- 有时候运行一次无法获取满24个小心心，**请设置多个时间不同的触发器！！！**  

## 0.7.3版本说明  
这是一个由[Huli-fox](https://github.com/Huli-fox) 对0.7.0版本进行优化的测试版本。    
主要优化内容有2方面：运行逻辑顺序和Server酱推送  
- **运行逻辑顺序优化**  
  - 旧顺序  ![旧顺序.jpg](https://s2.loli.net/2021/12/31/wvRB3JGYWEmCnou.jpg)  
  - 新顺序  ![新顺序.png](https://s2.loli.net/2022/01/01/7wedKYv9PC4NV6r.png)  
新顺序根据指定up（ruid）的粉丝勋章今日亲密度判断是否拿满了24个小心心（即1200亲密度为界），这种判断方法**要求用户尽量不要赠送24个小心心以外的礼物，否则可能引起代码失效**~~（彻底的白嫖）~~（因为技术力不够只能想出这种笨方法）  
新逻辑可能在一定程度上节约资源，如云函数的每月免费额度资源，本地运行的时间、流量资源  
- **Server酱推送优化**  
![推送.jpg](https://s2.loli.net/2022/01/01/XGNqVPecHE57y3R.jpg)  
上图中两条推送分别为0.7.0版本和0.7.3版本的推送  
使Server酱免费用户不用进入详情页即可知晓运行结果 ~~（将白嫖贯彻到底）~~  
本人技术力有限，此版本仍需测试与优化  

## 写在最后
在部署或使用过程中遇到什么问题，请首先**仔细**阅读文档，若发现自己实在无法解决的问题，可以提交Issues或者B站私信[@晓轩iMIKU](https://space.bilibili.com/32957695) 提问，提问时请带上详细的日志或者运行结果截图，以便快速解决问题！  
<sub>若对0.7.1-0.7.3版本有疑问，可联系[@一只大胡哩](https://space.bilibili.com/266441262)</sub>  
最后欢迎大家B站关注：  
[@嘉然今天吃什么](https://space.bilibili.com/672328094/) [@向晚大魔王](https://space.bilibili.com/672346917/) [@乃琳Queen](https://space.bilibili.com/672342685/) [@贝拉kira](https://space.bilibili.com/672353429/) [@珈乐Carol](https://space.bilibili.com/351609538/)  
<sub>ps:本项目夹带作者私货：每次执行时会随机关注一位A-SOUL成员（如果你没关注的话），若想取消此功能请注释掉代码中的某一行（嘿嘿~）</sub>
