# 本地部署
::: tip 提示
本教程将默认你会使用Git、Python、Linux等工具~  
🖐️会者不难  
使用Python 版本不低于**3.6**  
::: 

## 1.1 克隆本项目至本地并进入目录  
``` shell
git clone https://github.com/XiaoMiku01/bili-live-heart.git
cd bili-live-heart
```
## 1.2 安装所需模块  
``` shell
pip install -r requirements.txt
```

## 1.3 配置用户信息  
``` shell
vim user.toml
```
```
[[users]] # 账号1
# B站cookie(不要忘记双引号)
cookie = ""
# 需要自动打卡主播uid(不是房间号！是UID! 如果为0则只进行签到不赠送小心心 只能填一个)
ruid = 0

[[users]] # 账号2
cookie =""
ruid = 0

# 多账号请以相同格式添加

[cron] # Cron 表达式(五位数）
cron = ""

[serverchan] # Server酱sendkey(微信推送，选填)
sendkey = ""
```
::: tip 提示
cron 默认为 0 0 * * * 即每天0点0分运行  
补充：五位数Cron表达式，第一位表示分，第二位表示时，后三位本项目用不到不解释，例如：  
`10 0 * * *` 表示每天0点10分运行  
`30 8 * * *` 表示每天8点30分运行  
`50 20 * * *` 表示每天20点50分运行 
:::

## 1.4 运行脚本文件
``` shell
python3 index.py
```
::: tip 提示
本项目内置定时模块，并且默认在首次运行时执行一次，之后只需程序后台保持运行即可，可以使用screen tmux 等工具保持后台运行  
:::

# Docker

## 随手写的Dockerfile
没从环境拿变量，先填写配置再构建镜像的，反正能跑，开摆！
