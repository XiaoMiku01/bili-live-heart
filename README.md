<div align="center">

# **Bilibili粉丝牌助手**  

 </div>

基于Python3异步开发的自动获取每日小心心及直播间自动打卡脚本  
运行环境：不低于Python3.6  
***  

## 已实现功能  
> 直播区每日签到 ✅  
> 每日获取24个小心心 ✅  
> 指定房间每日弹幕打卡并赠送小心心 ✅  
> Server酱微信推送 ✅  

## 部署方式  
> ### 腾讯云函数版（**推荐🌟**）  
> >优点：  
免费、稳定、无需服务器、零基础部署  
缺点：  
由于腾讯云函数限制了最长15分钟运行时间，所以至少需要**9**个粉丝牌才能拿满24个小心心  

> ### 本地运行版  
> > 优点：  
没有粉丝牌数量限制  
缺点：  
需要自己搭建本地Python环境，设置定时任务  

## 详细教程  
- [获取B站Cookie](doc/bili.md)（**🌟这个很重要🌟**）  
- [Server酱推送](https://sct.ftqq.com/)（可选）  
- [腾讯云函数运行](doc/tencent_cloud.md) / [本地运行](doc/local.md)（二选一）  

## 写在最后
在部署或使用过程中遇到什么问题，请首先**仔细**阅读文档，若发现自己实在无法解决的问题，可以提交Issues或者B站私信[@晓轩iMIKU](https://space.bilibili.com/32957695)提问，提问时请带上详细的日志或者运行结果截图，以便快速解决问题！  
最后欢迎大家B站关注：  
[@嘉然今天吃什么](https://space.bilibili.com/672328094/) [@向晚大魔王](https://space.bilibili.com/672346917/) [@乃琳Queen](https://space.bilibili.com/672342685/) [@贝拉kira](https://space.bilibili.com/672353429/) [@珈乐Carol](https://space.bilibili.com/351609538/)  
<sub>ps:本项目夹带作者私货：每次执行时会随机关注一位A-SOUL成员（如果你没关注的话），若想取消此功能请注释掉代码中的某一行（嘿嘿~）</sub>