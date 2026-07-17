# Day 05 - 基础 Agent 与短期记忆

**日期：** 2026-07-16

## 今日目标

从普通的 LLM API 调用继续向 Agent 开发迈进，理解 Agent 的基本组成，并将 Day04 的命令行 Chatbot 封装成一个具有短期记忆的基础 Agent。

---

## 今日学习内容

### 1. Chatbot 与 Agent 的区别

普通 Chatbot 的基本流程：

```text
用户问题
→ LLM
→ 文字回答
```

Agent 的基本流程：

```text
用户目标
→ LLM 判断下一步
→ 执行动作或调用工具
→ 观察执行结果
→ 继续判断
→ 返回最终答案
```

理解到：

> Agent 的核心不只是拥有工具，而是能够围绕目标决定下一步行动，并通过循环使用工具和观察结果来完成任务。

可以暂时将 Agent 的基本组成概括为：

```text
Agent = LLM + Prompt + Memory + Tools + Agent Loop
```

---

### 2. 理解工具的作用

Tool 是程序提供给模型使用的外部能力。

例如：

- 计算器；
- 天气 API；
- 网页搜索；
- 文件操作；
- 数据库查询。

模型负责判断是否需要工具，以及生成工具名称和参数；真正的工具执行由 Python 程序完成。

例如，一个计算任务可以分解为：

```text
LLM 判断需要精确计算
→ 申请 calculator
→ Python 执行计算
→ 工具返回结果
→ LLM 分析并组织最终回答
```

---

### 3. 理解 Agent Loop

Agent Loop 是处理一个用户任务时，模型反复决策、执行和观察的内部循环：

```python
while True:
    response = call_llm(messages)

    if response 需要工具:
        result = execute_tool()
        messages.append(result)
    else:
        return response 最终答案
```

区分了两种不同的循环：

| 循环 | 作用 | 结束条件 |
| --- | --- | --- |
| 对话循环 | 持续接收用户的新问题 | 用户输入 `exit` 或 `quit` |
| Agent Loop | 完成当前这一个任务 | 模型不再申请工具并给出最终答案 |

理解到：

> `exit` 和 `quit` 结束的是命令行对话程序，而不是一次任务内部的 Agent Loop。

---

### 4. 理解无状态 API

DeepSeek API 本身是无状态的，服务端不会自动记住上一次请求的对话内容。

API Key 的作用是身份认证：

```text
你是谁，以及是否有调用权限
```

`messages` 的作用是携带对话状态：

```text
之前的用户消息和模型回答是什么
```

因此：

```text
API Key
→ 身份认证

messages
→ 对话历史

Python 程序
→ 状态管理者
```

如果第二次请求没有重新发送第一次的消息，模型就无法根据之前的信息继续回答。

---

### 5. messages 与短期记忆

每轮对话都将用户消息和模型回答加入同一个列表：

```python
self.messages.append({
    "role": "user",
    "content": user_input,
})

self.messages.append({
    "role": "assistant",
    "content": answer,
})
```

下一次调用 API 时，程序重新发送完整的 `messages`，模型因此能够读取之前的上下文。

测试对话：

```text
用户：我的名字叫小明
助手：你好，小明
用户：我叫什么名字？
助手：你叫小明
```

理解到：

> Memory 不是模型自动永久保存的信息，而是程序保存并在每次请求中重新发送的上下文。

只保存用户消息是不完整的，因为模型将看不到自己之前的回答，可能无法理解“你刚才给出的第二个方案”等引用，也可能重复或产生前后矛盾的内容。

---

### 6. 为什么是短期记忆

随着历史增长：

- 输入 Token 增加；
- 调用成本增加；
- 响应可能变慢；
- 最终可能超过模型的上下文窗口；
- 过多无关历史可能影响有效信息的利用。

因此，直接保存完整 `messages` 更适合作为短期记忆。

后续可以学习：

- 对话摘要；
- 记忆检索；
- 长期存储；
- RAG。

---

### 7. 使用 Agent 类封装调用流程

创建了：

```text
week01/day05/basic_agent.py
```

使用 `Agent` 类保存：

```python
self.headers
self.messages
```

`run()` 方法负责：

```text
接收用户输入
→ 保存 user 消息
→ 调用 DeepSeek API
→ 解析模型回答
→ 保存 assistant 消息
→ 返回回答
```

命令行入口负责：

- 创建并复用同一个 Agent；
- 持续接收用户输入；
- 支持 `exit` 和 `quit`；
- 跳过空输入；
- 捕获基本的请求异常。

最终成功验证了连续对话和基于 `messages` 的短期记忆。

---

## 今日概念修正

### Agent 不只是 LLM 加工具

工具是 Agent 的重要组成，但更关键的是模型能够根据目标决策，并通过 Agent Loop 观察工具结果、继续行动。

### API 无状态与 API Key 无关

无状态指服务端不会自动保留上一次请求的对话内容；API Key 只用于认证。

### 对话循环不等于 Agent Loop

对话循环处理多个用户问题；Agent Loop 在一次任务内部持续行动，直到获得最终答案。

---

## 今日最大收获

今天最大的收获是理解了 Agent 的基础运行方式，并第一次将零散的 LLM API 调用封装为一个能够维护状态的对象。

核心认识：

```text
模型本身不会自动记住对话
→ Python 保存 messages
→ 每次请求重新发送历史
→ 模型表现出上下文记忆
```

这为后续实现 Tool Calling 和真正的 Agent Loop 打下了基础。

---

## 下一步计划

- 使用环境变量管理 API Key；
- 编写第一个计算器工具；
- 使用 JSON Schema 描述工具；
- 解析模型返回的 `tool_calls`；
- 将工具结果返回给模型；
- 实现第一个完整的工具型 Agent Loop。
