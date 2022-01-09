# 本地运行教程  
注意：此方法需要一些基础，例如Python的安装和使用，git的使用，Linux定时任务将不再赘述，若是小白请使用[腾讯云函数部署](tencent_cloud.md)  
**使用的Python版本必须大于3.6**

## 第一步：
下载源码  
```shell
git clone https://github.com/XiaoMiku01/bili-live-heart.git
```  

## 第二步：
安装第三方库  
```
pip install -r requirements.txt
```
进入目录 编辑`user.tom`l文件  
```
[users]
# 自己B站uid
uid = 123
# B站cookie(不要忘记双引号)
cookie = ""
# 需要自动打卡主播uid(如果为0则只进行签到不赠送小心心)
ruid = 0

# Server酱sendkey（微信推送，选填）
sendkey = ""
```  
## 第三步：
运行`index.py`文件  
```
python index.py
```

## 第四步：
若正常运行，请自行设置定时任务  

# 完