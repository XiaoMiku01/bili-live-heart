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

## 1.5 本地更新  
本地更新：命令行直接运行命令拉取最新仓库即可  
 ```
 git fetch origin master //从远程主机的master分支拉取最新内容 
git merge FETCH_HEAD    //将拉取下来的最新内容合并到当前所在的分支中
 ```

# Docker

## 2.1 拉取Docker镜像至本地
``` shell
docker pull xiaomiku01/bili-live-heart
```
## 2.2 配置用户信息
创建文件env.list，具体内容参考本地部署的部分
```
# B站cookie
COOKIE=""
# 需要自动打卡主播uid
RUID=0
# Cron 表达式
CRON="0 0 * * *"
# Server酱sendkey，选填
SERVER_CHAN_SENDKEY=""
```
::: tip 提示
在docker模式下不支持多用户，可以通过并行启动多个容器来达到多用户的目的
:::
## 2.3 创建并运行容器
``` shell
docker run -d -name bili-live-heart1 --env-file env.list xiaomiku01/bili-live-heart
```
如果不希望创建env.list文件，此处也可以把用户配置直接写在命令里
``` shell
docker run -d -name bili-live-heart1 -e COOKIE="" -e RUID=0 -e CRON="0 0 * * *" -e SERVER_CHAN_SENDKEY="" xiaomiku01/bili-live-heart
```
## 2.4 本地更新
docker本身没有更新机制，更新容器需要停止并删除容器，重新拉取镜像并重建容器
``` shell
docker stop bili-live-heart1
docker rm bili-live-heart1
docker pull xiaomiku01/bili-live-heart
docker run -d -name bili-live-heart1 --env-file env.list xiaomiku01/bili-live-heart
```
不过这里也可以讨个巧，在docker运行中进入容器中通过git更新代码，然后重启容器，虽然也比较麻烦，但似乎要好一点
``` shell
docker exec -it -w /app/bili-live-heart bili-live-heart1 git pull
docker restart bili-live-heart1
```
