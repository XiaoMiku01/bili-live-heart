# OnePush使用指南  
:::tip 不适合0基础小白:::  
## 项目地址：  
[OnePush](https://github.com/y1ndan/onepush)  
支持 Bark App、酷推、钉钉机器人、Discord、iGot聚合推送、pushplus、Server酱、Telegram robot、企业微信应用、企业微信机器人和自定义推送  

:::tip OnePush推送参数一览  
推送名称 / notifier: bark  
参数大全 / params:  
{'required': ['key'], 'optional': ['title', 'content', 'sound', 'isarchive', 'icon', 'group', 'url', 'copy', 'autocopy']}  
  
推送名称 / notifier: custom  
参数大全 / params:  
{'required': ['url'], 'optional': ['method', 'datatype', 'data']}  
  
推送名称 / notifier: dingtalk  
参数大全 / params:  
{'required': ['token'], 'optional': ['title', 'content', 'secret', 'markdown']}  
  
推送名称 / notifier: discord  
参数大全 / params:  
{'required': ['webhook'], 'optional': ['title', 'content', 'username', 'avatar_url', 'color']}  
  
推送名称 / notifier: pushplus  
参数大全 / params:  
{'required': ['token', 'content'], 'optional': ['title', '‎主题‎', 'markdown']}  
  
推送名称 / notifier: qmsg  
参数大全 / params:  
{'required': ['key'], 'optional': ['title', 'content', 'mode', 'qq']}  
  
推送名称 / notifier: serverchan  
参数大全 / params:  
{'required': ['sckey', 'title'], 'optional': ['content']}  
  
推送名称 / notifier: serverchanturbo  
参数大全 / params:  
{'required': ['sctkey', 'title'], 'optional': ['content', 'channel', 'openid']}  
  
推送名称 / notifier: telegram  
参数大全 / params:  
{'required': ['token', 'userid'], 'optional': ['title', 'content', 'api_url']}  
  
推送名称 / notifier: wechatworkapp  
参数大全 / params:  
{'required': ['corpid', 'corpsecret', 'agentid'], 'optional': ['title', 'content', 'touser', 'markdown']}  
  
推送名称 / notifier: wechatworkbot  
参数大全 / params:  
{'required': ['key'], 'optional': ['title', 'content', 'markdown']}  
  
例子  
telegram  
ONEPUSH={"notifier":"telegram","params":{"markdown":false,"token":"xxxx","userid":"xxx"}}  
  
discord  
ONEPUSH={"notifier":"discord","params":{"markdown":true,"webhook":"https://discord.com/api/webhooks/xxxxxx"}}  
  
注：markdown参数设置为True可优化推送消息排版  
:::  
