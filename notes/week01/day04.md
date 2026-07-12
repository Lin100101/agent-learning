# Day 04 - LLM API 调用与第一个 AI ChatBot

**日期：** 2026-07-12

## 今日目标

学习如何调用大语言模型（LLM）API，理解 AI 应用的基本工作流程。

通过调用 DeepSeek API，实现第一个支持上下文记忆的命令行 AI 聊天机器人。

---

## 今日学习内容

## 1. 理解 LLM API 的基本工作流程

学习了大语言模型 API 的调用方式。

整体流程：

```text
Python 程序

↓

HTTP POST 请求

↓

LLM API 服务

↓

模型推理

↓

返回 JSON 响应

↓

Python 解析结果
```

理解到：

AI API 并不是返回固定的数据，而是根据用户提交的信息进行推理，并生成对应响应。

---

## 2. 理解 POST 请求结构

调用 LLM API 时，需要发送 POST 请求。

一次请求主要包含：

```text
URL

Header

Body(JSON)
```

---

### URL

用于指定 API 接口。

例如：

```text
https://api.deepseek.com/chat/completions
```

不同 URL 通常对应不同功能。

---

### Header

用于描述请求信息。

例如：

```python
headers = {
    "Authorization": "Bearer API_KEY",
    "Content-Type": "application/json"
}
```

作用：

* `Authorization`：身份验证
* `Content-Type`：告诉服务器请求数据使用 JSON 格式

理解到：

认证信息通常放在 Header 中，而不是 Body 中。

---

### Body

用于提交实际请求内容。

例如：

```python
data = {
    "model": "deepseek-v4-pro",
    "messages": [...]
}
```

其中包含：

* 使用的模型
* 用户输入
* 对话历史

---

# 3. 理解 messages 与上下文（Context）

学习了 LLM API 中最重要的概念：

`messages`。

它代表发送给模型的聊天历史。

结构：

```python
messages = [
    {
        "role": "user",
        "content": "你好"
    },
    {
        "role": "assistant",
        "content": "你好，有什么可以帮助你的吗？"
    }
]
```

理解：

* 一个 message 使用字典表示；
* 多个 message 使用列表保存。

原因：

聊天不是单条消息，而是一系列连续交互。

---

## 4. 理解模型上下文机制

认识到：

模型本身不会自动保存聊天记录。

每次 API 请求时，客户端需要重新发送：

```python
messages
```

因此：

聊天机器人实际上由程序维护状态：

```text
用户输入

↓

保存 message

↓

发送完整上下文

↓

模型生成回复

↓

保存 assistant 回复
```

---

## 5. 理解 Token 与上下文长度

学习了 Token 的概念。

API 返回：

```python
usage
```

其中包含：

* `prompt_tokens`
* `completion_tokens`
* `total_tokens`

理解：

* prompt_tokens：发送给模型的信息量
* completion_tokens：模型生成的信息量
* total_tokens：两者总和

---

进一步理解：

随着聊天记录增加：

```text
messages
越来越长

↓

prompt_tokens 增加

↓

成本增加

↓

可能超过上下文限制
```

因此实际 Agent 系统通常会使用：

* Conversation Summary（对话摘要）
* Memory Retrieval（记忆检索）
* RAG（检索增强生成）

来管理长期上下文。

---

# 6. 理解 API 返回 JSON 结构

学习分析 API 返回结果。

典型结构：

```text
response.json()

↓

choices(list)

↓

message(dict)

↓

content(str)
```

获取模型回复：

```python
answer = response.json()["choices"][0]["message"]["content"]
```

理解：

### choices

表示模型生成的候选回答列表。

其中：

```python
index
```

表示候选回答编号，而不是聊天轮数。

---

### usage

用于统计 Token 消耗。

帮助开发者：

* 控制成本；
* 优化上下文；
* 调整模型调用策略。

---

# 7. 实现第一个 AI ChatBot

最终实现了一个命令行聊天机器人。

实现功能：

* 用户输入问题；
* 调用 DeepSeek API；
* 输出 AI 回复；
* 保存聊天上下文；
* 支持连续对话；
* 支持退出命令。

核心流程：

```text
用户输入

↓

messages 添加 user

↓

发送 API 请求

↓

解析 AI 回复

↓

messages 添加 assistant

↓

继续下一轮聊天
```

---

# 8. Code Review 与工程实践

通过代码优化，学习了一些软件工程习惯。

## 配置与逻辑分离

将：

```python
URL
HEADERS
MODEL
```

提取为独立变量。

提高代码可维护性。

---

## 错误处理意识

认识到：

请求不一定成功。

需要：

* 检查 status_code；
* 处理网络异常；
* 防止程序直接崩溃。

---

## API Key 安全

认识到：

API Key 类似密码。

不能直接写入公开代码。

后续应该使用：

* 环境变量；
* `.env` 文件；

进行管理。

---

# 今日最大收获

今天最大的收获：

> 理解了 LLM 应用的基本运行机制，并第一次独立实现了一个具有上下文能力的 AI 聊天机器人。

相比普通 Python 程序：

```text
输入

↓

处理

↓

输出
```

AI 应用增加了：

```text
上下文管理

↓

模型推理

↓

动态生成结果
```

这是从传统程序开发进入 AI 应用开发的重要一步。

---

# 今日反思

今天让我认识到：

调用 AI API 并不只是发送一个请求。

真正的 AI 应用开发需要理解：

* 网络通信；
* 数据结构；
* 上下文管理；
* Token 成本；
* 状态维护。

这些基础知识会直接影响后续 Agent 系统的设计。

---

# 明日计划

* 学习 `.env` 管理 API Key
* 学习函数封装，提高代码结构
* 学习异常处理 `try...except`
* 学习 Streaming 流式输出
* 优化 ChatBot 代码结构
