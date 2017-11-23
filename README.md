## 微信聊天机器人 
基于 [itchat](https://github.com/littlecodersh/ItChat) 和 [图灵机器人](http://www.tuling123.com)。

## 功能
* 个人聊天时调用图灵机器人免费api（1000次/天），自动回复
* 群聊中需要@机器人登录的用户后面跟聊天内容
    
    例如在群聊中输入
    `@Mio 杭州天气`
* 输入猜数字可开始游戏，按用户名区分，可多用户同时开始猜数字



## 使用方法
* `git clone `本项目
* 安装Python依赖包，推荐使用虚拟环境 virtualenv或conda

    ```
    virtualenv yvo-wechat
    source yvo-wechat/bin/activate
    ```
    
    安装依赖包
    
    ```
    pip install -r requirements.txt
    ```
* 启动

    ```shell
    python tuling.py
    // 会出现二维码
    ```
    
    打开微信扫描终端出现的二维码
    
    
