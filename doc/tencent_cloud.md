# 腾讯云函数部署教程（**推荐🌟**）
## 第一步：  
下载云函数压缩包(二选一)  
- [Github](https://github.com/XiaoMiku01/bili-live-heart/releases/tag/zip)
- [百度云](https://pan.baidu.com/s/1sFzW5FHTtUYi_sxy0ZtVxg)  
## 第二步：
- 登录[腾讯云函数官网](https://cloud.tencent.com/product/scf) 并进入控制台![YZJ1L__V_9J2S_7OK8HM896.png](https://i.loli.net/2021/10/29/etvOPIGRZ3YFbU1.png)  
- 选择函数服务 - 新建![XF~GC_UOPY_9SZM_L_F8D_1.png](https://i.loli.net/2021/10/29/8RUAnYovkB5fMGy.png)  
- 选择自定义创建 - 事件函数-函数名称随意-地域国内随意 - 代码部署 - 运行环境选择Python3.6![O_6_`TF02ZX1OFD5__Z@TJ7.png](https://i.loli.net/2021/10/29/XZFUd7wJNBlCQGh.png)  
- 提交方法选择本地上传zip包 - 执行方法**默认不要改** - 函数代码上传刚刚下载的压缩包![_PU1N_1K539U_C~_EE85~PP.png](https://i.loli.net/2021/10/29/tI8PKhWY6nTO1vC.png)  
- 点开高级配置 - 环境配置  
执行超时时间：**900**秒  
环境变量填写自己B站uid，B站cookie（[获取方式](bili.md)），需要赠送小心心的主播uid（ruid），Server酱的[SendKey](https://sct.ftqq.com)（选填）（注意：**key栏中的字母全为小写**）![_DVA669_BPQ_BC~NSULLUDE.png](https://i.loli.net/2021/10/29/tzPvoufASYh9ZD3.png)
- 其他配置不变 - 展开触发器配置  
选择自定义创建 - 触发方式：定时触发 - 触发周期：每一天或自定义（自定义需要填写Cron表达式（[文档](https://cloud.tencent.com/document/product/583/9708#cron)）- 立即启用打钩✅ - 点击右下角完成![RO~8B_E5AE_A_24TYF5FI~U.png](https://i.loli.net/2021/10/29/2vieBExYJSnluF7.png)  
- 待创建成果后点击立即转跳 - 函数代码 - 左下角 - 测试![NQNA@W_LIV5X_~CEV_4EIVW.png](https://i.loli.net/2021/10/29/JAFTWgXD9VxGBQP.png)  
![FQ_I5F7@6JJSY_7RP8TNNM8.png](https://i.loli.net/2021/10/29/5CzGQDIfiZTnypw.png)  
![6_UD_~MIY@DI30NI0_PO8VY.png](https://i.loli.net/2021/10/29/lk9ADWO1dNreXLY.png)
- 耐性等待10-15分钟，查看返回日志是否运行成功![~QCH3OAULJ_2U3_~@Y_7R8S.png](https://i.loli.net/2021/10/29/up92xcgNa4vHjIk.png)  
# 完