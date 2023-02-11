# SocketChatGPT



基于 Socket 的 OpenAI GPT-3 消息处理模块，兼容 cqhttp qq bot 报文格式



Fork 自 Mirai qq ChatGPT 项目  [timlzh/QChatBot-GPT](https://github.com/timlzh/OPQChatBot-GPT)

仓库源 [Byaidu/QChatBot-GPT](https://github.com/Byaidu/QChatBot-GPT)



## 环境配置 



### 依赖

transformers

openai



### 配置文件

请参考 config.json:

defaultApiKey: 公共 API key

bind_ip: 绑定地址

port: 绑定端头

openai_proxy: 代理地址



## 使用方法



使用 `python bot.py` 启动主程序

用 socket 传入包含 “message” 和 “group_id” 关键字的 json 消息，其中 group_id 为分组 ID （int 类型）

等待回复，该回复为 chatGPT 的回复语句



## 使用方法



```
OPQChatBot-GPT 指令列表

/chat  ：生成对话
/clear  ：重置对话
/get   ：查看配置
/reset  ：重置配置
/preset ：修改预设
/key   ：设置 OpenAI API Key
/mem   ：设置记忆长度，范围为 4~4096
/help  ：查看帮助

配置参考 ：https://beta.openai.com/docs/api-reference/completions/create
```

