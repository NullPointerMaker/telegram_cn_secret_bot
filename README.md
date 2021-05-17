# Telegram CN Secret Bot
Telegram 机器人：个人消息自毁。

## 使用
加入群组并赋予删除消息权限。  
发送 `/lifetime n` 为 `n` 秒后删除消息。  
发送 `/lifetime 0` 为不删除消息。

## 部署
请先使用 [@BotFather](https://t.me/botfather) 生成一个机器人并获得 API Token。  
再将 API Token 填入 `token` 文件。  
在操作系统中安装 Python 运行环境。  
Windows 执行 `Telegram-CNSecretBot.Cmd` 文件。  
其它操作系统执行 `telegram-cn-secret-bot.bash` 文件。