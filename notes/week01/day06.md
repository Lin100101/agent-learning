# Day 06 - Tool Calling 与计算器工具

**日期：** 2026-07-17

## 今日目标

在 Day05 基础 Agent 和短期记忆的基础上，开始学习 Tool Calling，并实现第一个可由模型选择的计算器工具。

今日重点不是使用 Agent 框架，而是理解模型、Python 程序和工具之间的消息传递过程。

---

## 今日学习内容

### 1. 使用环境变量管理 API Key

通过环境变量读取 DeepSeek API Key：

```python
api_key = os.getenv("DEEPSEEK_API_KEY")
```

理解到：

- API Key 不应该直接写入代码；
- PowerShell 中通过 `$env:DEEPSEEK_API_KEY` 设置的是当前终端的临时环境变量；
- 新开或关闭终端后，临时环境变量不会继续存在；
- 可以设置用户级环境变量，让新终端也能读取；
- 不应在控制台、日志或 Git 仓库中暴露真实 API Key。

---

### 2. 编写受限的计算器工具

实现了一个支持加、减、乘、除的计算器函数：

```python
def calculator(num1, num2, operation):
    ...
```

工具只允许以下操作：

```text
add
subtract
multiply
divide
```

同时增加了除数不能为零和未知运算类型的检查。

---

### 3. 理解 eval 的安全风险

`eval()` 会把字符串当作 Python 表达式执行。

它不会主动扫描环境变量，但如果传入的字符串要求读取环境变量，它可能执行对应表达式并泄露 API Key 等敏感信息。

理解到：

> 用户输入和模型输出都属于不可信数据，不能直接当作代码执行。

这种风险与 SQL 注入具有相似的根本原因：外部数据突破了数据边界，被解释器当作指令执行。

因此计算器采用固定参数和允许列表，而不是直接执行 `eval(expression)`。

---

### 4. 使用 JSON Schema 描述工具

使用 `TOOLS` 向模型说明计算器的：

- 名称；
- 用途；
- 参数名称；
- 参数类型；
- 必填参数；
- 运算类型的允许范围。

核心结构：

```text
工具
└── function
    ├── name
    ├── description
    └── parameters
        ├── type
        ├── properties
        └── required
```

使用 `enum` 将 `operation` 限制为程序支持的四种运算，减少模型生成无效参数的可能性。

---

### 5. 理解 tool_choice

学习了以下设置：

| 设置 | 含义 |
| --- | --- |
| `none` | 禁止模型申请工具 |
| `auto` | 模型自行决定直接回答还是申请工具 |
| `required` | 模型必须申请一个或多个工具 |
| 指定函数 | 模型必须申请指定工具 |

理解到：

> `tool_choice` 只控制模型是否生成工具调用请求，不会替 Python 执行工具。

数学问题在 `auto` 模式下仍然调用计算器是正常行为，因为模型判断该工具适合完成任务。

---

### 6. 解析 tool_calls

从模型响应中读取：

```python
tool_calls = message.get("tool_calls")
```

进一步取得：

```text
tool_call_id
tool_name
arguments
```

其中 `arguments` 是 JSON 字符串，需要使用：

```python
json.loads(...)
```

转换为 Python 字典。

`tool_call_id` 每次调用都会变化，它用于将工具结果与模型本次发出的工具请求对应起来，不能在代码中写死。

---

### 7. 执行计算器并保存工具消息

当前代码已经能够：

1. 接收用户的计算请求；
2. 让模型选择 `calculator`；
3. 解析模型生成的参数；
4. 由 Python 执行计算器函数；
5. 保存模型的 `assistant/tool_calls` 消息；
6. 使用动态 `tool_call_id` 保存 `role="tool"` 的计算结果。

当前已经形成：

```text
user
→ assistant/tool_calls
→ tool/result
```

---

## 今日调试记录

曾在一次计算请求后继续对话时遇到：

```text
400 Bad Request
```

原因是工具消息链不完整：程序添加了 `role="tool"` 消息，却没有按照协议保存模型的工具调用请求、对应的 `tool_call_id` 和实际执行结果。

正确顺序应该是：

```text
user
→ assistant（包含 tool_calls）
→ tool（包含对应的 tool_call_id 和结果）
→ assistant（最终回答）
```

理解到：

> 工具调用不是一条孤立消息，而是一组具有严格顺序和对应关系的消息。

---

## 今日最大收获

今天最大的收获是理解了 Tool Calling 的职责边界：

```text
LLM 决定调用哪个工具以及传入什么参数
→ Python 验证并执行工具
→ Python 将结果返回给 LLM
→ LLM 根据结果生成最终回答
```

模型并不会直接运行 Python 函数，真正的执行权始终在程序中。

---

## 当前未完成

今天停在工具结果已经写入 `messages` 的位置，尚未完成：

- 将工具结果再次发送给模型；
- 保存模型根据工具结果生成的最终回答；
- 使用循环支持连续的工具调用；
- 增加最大工具调用次数；
- 验证工具名称和模型生成的参数；
- 完善工具执行异常处理。

---

## 下一步计划

1. 完成 `tool/result → assistant/final answer` 消息链；
2. 测试工具调用后的普通对话是否正常；
3. 将单次工具处理扩展成完整 Agent Loop；
4. 增加最大循环次数和工具参数验证；
5. 整理并补充 Day05 学习笔记。
