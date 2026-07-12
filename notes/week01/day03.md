# Day 03 - HTTP 请求、API 调用与 JSON 数据解析

**日期：** 2026-07-10

## 今日目标

学习 Python 如何与外部服务进行通信。

理解 HTTP 请求、API 调用流程以及 JSON 数据在 Python 中的处理方式，为后续调用大模型 API 做准备。

---

## 今日学习内容

### 1. 使用 requests 发送 HTTP 请求

学习了 Python 第三方库：

```python
import requests
```

通过 requests 可以方便地发送 HTTP 请求。

例如：

```python
response = requests.get(url)
```

服务器返回的数据会保存在：

```python
response
```

对象中。

---

### 2. 理解 HTTP 请求与响应

一次完整的 HTTP 通信：

```text
客户端

↓

发送 Request

↓

服务器处理

↓

返回 Response

↓

客户端解析
```

Response 对象包含：

* status_code
* headers
* text
* json()

等信息。

---

### 3. 理解 status_code

学习了 HTTP 状态码的作用。

例如：

```python
response.status_code
```

表示服务器处理请求后的结果。

常见状态：

* 200：请求成功
* 404：资源不存在
* 500：服务器错误

理解到：

如果能够获得 status_code，说明客户端和服务器之间已经建立通信。

---

### 4. 理解 response.json()

学习：

```python
response.json()
```

作用：

将服务器返回的 JSON 数据转换为 Python 对象。

例如：

JSON：

```json
{
    "name": "Python"
}
```

转换为：

```python
{
    "name": "Python"
}
```

Python 中对应：

```python
dict
```

---

### 5. JSON 与 Python 数据结构

学习了 JSON 和 Python 类型之间的对应关系：

| JSON    | Python    |
| ------- | --------- |
| object  | dict      |
| array   | list      |
| string  | str       |
| number  | int/float |
| boolean | bool      |

理解到：

API 返回的数据，本质上就是嵌套的 Python 字典和列表。

---

### 6. 调试 HTTP 请求问题

遇到了 requests 请求异常：

```text
SSL Error
```

通过错误信息定位问题。

学习到：

调试程序时应该：

1. 阅读 traceback；
2. 找到错误发生的位置；
3. 分析错误原因；
4. 验证解决方案。

错误信息不是阻碍，而是程序提供的重要线索。

---

### 7. 分析 API 返回结构

观察 API 返回的数据：

```python
dict_keys([
    "args",
    "headers",
    "origin",
    "url"
])
```

开始理解：

服务器返回的数据通常具有明确结构。

开发者需要：

* 查看 key；
* 理解字段含义；
* 提取需要的信息。

---

## 今日最大收获

今天最大的收获：

> 理解了程序如何通过 HTTP 与外部世界进行通信。

以前：

代码只是运行在本地。

今天：

理解了：

```text
Python程序

↓

网络请求

↓

服务器

↓

返回数据

↓

Python解析
```

这为后续调用 AI API 打下了基础。

---

## 今日反思

今天开始从单机编程进入网络编程。

认识到：

现代软件并不是孤立运行的。

大量应用都依赖：

* API
* 网络通信
* 数据交换

理解 HTTP 和 JSON，是连接各种服务的重要基础。

---

## 明日计划

* 学习 LLM API 调用流程
* 理解 Header、Body、Authorization
* 调用 DeepSeek API
* 学习 messages 与上下文管理
