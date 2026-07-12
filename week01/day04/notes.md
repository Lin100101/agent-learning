# Day 04 学习笔记 —— 第一次调用 LLM API

## 今日目标

学习如何使用 Python 调用大语言模型（LLM）API，并理解其工作原理，而不仅仅是会复制示例代码。

---

# 一、GET 与 POST

## GET

用于**获取资源**。

例如：

* 获取网页
* 查询天气
* 获取用户信息

```python
requests.get(url)
```

特点：

* 通常不需要提交大量数据。
* 更适合查询操作。

---

## POST

用于**向服务器提交数据**。

AI API 基本都使用 POST。

```python
requests.post(url, headers=headers, json=data)
```

原因：

模型不仅需要知道"我要聊天"，还需要知道：

* 使用哪个模型
* 用户输入是什么
* 参数（temperature、max_tokens 等）

这些都需要通过 POST 提交给服务器。

---

# 二、HTTP 请求组成

一次 HTTP POST 请求主要包含三部分：

```
POST URL

Header
↓

Body(JSON)
↓

Server
```

## URL

决定访问哪个接口（API Endpoint）。

例如：

```
https://api.deepseek.com/chat/completions
```

URL 可以理解为服务器提供的不同"窗口"。

---

## Header（请求头）

用于描述请求本身。

例如：

```python
headers = {
    "Authorization": "Bearer xxx",
    "Content-Type": "application/json"
}
```

主要作用：

* 身份认证（Authorization）
* 数据格式说明（Content-Type）

Header 更像"信封外的信息"。

---

## Body（请求体）

真正发送给服务器的数据。

例如：

```python
{
    "model": "...",
    "messages": [...]
}
```

Body 更像"信件内容"。

---

# 三、JSON 请求体

请求体主要包含：

```python
data = {
    "model": "deepseek-v4-pro",
    "messages": [...]
}
```

## 为什么 messages 是列表？

因为聊天不是一句话。

聊天历史可能是：

```
User
Assistant
User
Assistant
```

因此：

* 一个 message 是一个字典
* 多个 message 使用列表保存

例如：

```python
[
    {
        "role": "user",
        "content": "你好"
    },
    {
        "role": "assistant",
        "content": "你好！"
    }
]
```

---

## 为什么一个 message 是字典？

因为一条消息不仅有内容，还有属性。

例如：

```python
{
    "role": "user",
    "content": "你好"
}
```

其中：

* role：是谁说的话
* content：说了什么

---

# 四、什么是上下文（Context）

聊天模型并不会自动记住之前聊天内容。

真正保存聊天记录的是客户端程序。

每次请求都会重新发送整个 messages。

例如：

第一次：

```
User
```

第二次：

```
User
Assistant
User
```

第三次：

```
User
Assistant
User
Assistant
User
```

模型之所以能回答连续问题，是因为每次请求都重新获得了完整聊天历史。

---

# 五、为什么 Token 会越来越多？

因为每一次请求都会重新发送整个 messages。

例如：

第一轮：

```
User
```

第二轮：

```
User
Assistant
User
```

第三轮：

```
User
Assistant
User
Assistant
User
```

因此：

* prompt_tokens 会不断增加。
* API 成本也会不断增加。
* 上下文过长最终会超过模型的 Context Window。

今天还讨论了两种解决方案：

1. Conversation Summary（对话摘要）
2. Memory Retrieval / RAG（按需检索相关记忆）

这也是 Agent 中 Memory 的核心思想。

---

# 六、response.json() 结构

API 返回的是 JSON。

解析后得到 Python 字典。

主要结构：

```python
response.json()

↓

choices（列表）

↓

message（字典）

↓

content（真正回答）
```

获取模型回复：

```python
answer = response.json()["choices"][0]["message"]["content"]
```

其中：

* choices：多个候选回答
* index：候选回答编号（不是聊天轮数）
* message：模型回复
* usage：Token 使用情况

---

# 七、完成了第一个 AI ChatBot

最终实现了一个支持：

* 连续聊天
* 保存上下文
* 输入 exit / quit 退出
* HTTP 状态码检查
* 常量配置（URL、HEADERS、MODEL）

的命令行聊天机器人。

程序流程：

```
用户输入

↓

messages 添加 user

↓

POST 请求

↓

解析 JSON

↓

messages 添加 assistant

↓

输出回答

↓

继续聊天
```

---

# 八、Code Review 收获

通过代码 Review，学习了几个软件工程实践：

* 常量使用全大写命名（URL、HEADERS、MODEL）
* 先检查 status_code，再解析 JSON
* 保存 assistant 回复，保持上下文完整
* API Key 不应写入公开代码，应使用环境变量管理
* 程序应考虑异常处理（try...except）

---

# 今日总结

今天不仅学会了如何调用大模型 API，更重要的是理解了 LLM API 的底层工作方式。

最大的收获有三点：

1. 理解了 HTTP 请求（URL、Header、Body）的组成。
2. 理解了 messages 如何维护聊天上下文，以及为什么 Token 会不断增长。
3. 独立实现了一个支持上下文的命令行 AI 聊天机器人。

这意味着我已经具备了开发基础 AI 应用的能力，为后续学习 Agent、LangChain、LangGraph 和 Memory 等内容打下了坚实基础。
