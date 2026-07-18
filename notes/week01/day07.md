# Day 07 - 完整 Agent Loop 与安全限制

**日期：** 2026-07-18

## 今日目标

在 Day06 计算器 Tool Calling 的基础上，补全工具结果返回 LLM 的消息链，将固定的两次模型调用升级为真正的 Agent Loop，并增加必要的错误处理与安全限制。

---

## 今日学习内容

### 1. 补全 Tool Calling 消息链

Day06 已经能够让模型申请计算器，并由 Python 执行工具，但当时程序直接将计算结果返回给用户。

今天补全了最后一步：将工具结果再次发送给 LLM，由模型结合结果生成最终自然语言回答。

完整消息顺序：

```text
user
→ assistant/tool_calls
→ tool/result
→ assistant/final answer
```

理解到：

> 工具结果必须通过带有对应 `tool_call_id` 的 `role="tool"` 消息返回，模型才能将结果与之前的工具请求对应起来。

---

### 2. 提取 call_llm 方法

将重复的 API 请求逻辑提取为：

```python
def call_llm(self):
    ...
```

`call_llm()` 只负责：

```text
组装请求数据
→ 调用 LLM API
→ 检查 HTTP 状态
→ 返回模型 message
```

`run()` 则负责决定如何处理模型返回的普通回答或工具请求。

通过这一调整，模型通信与 Agent 流程控制的职责更加清晰。

---

### 3. 当前代码架构

当前程序可以划分为五个部分：

```text
agent_loop.py
│
├── 配置
│   ├── URL
│   ├── MODEL
│   ├── MAX_STEPS
│   └── MAX_TOOL_CALLS
│
├── 工具实现
│   └── calculator()
│
├── 工具说明
│   └── TOOLS
│
├── Agent
│   ├── __init__()
│   ├── call_llm()
│   └── run()
│
└── 程序入口
    └── main()
```

职责划分：

```text
main()       → 管理终端交互
run()        → 管理任务流程
call_llm()   → 管理模型通信
calculator() → 执行实际计算
TOOLS        → 向模型描述工具
messages     → 保存完整对话与工具消息
```

---

### 4. 从固定请求升级为 Agent Loop

之前的程序假设：

```text
第一次调用 LLM → 申请工具
第二次调用 LLM → 一定返回最终答案
```

这个假设并不可靠，因为模型在获得一次工具结果后，仍可能继续申请其他工具。

今天使用循环实现：

```python
for step in range(MAX_STEPS):
    message = self.call_llm()
    tool_calls = message.get("tool_calls")

    if not tool_calls:
        保存最终回答
        return answer

    执行工具并保存结果
```

循环逻辑：

```text
调用 LLM
→ 没有 tool_calls：返回最终答案并结束
→ 存在 tool_calls：执行工具并继续下一轮
```

理解到：

> Agent Loop 不预先规定调用 LLM 的固定次数，而是根据每轮模型响应决定继续行动还是结束任务。

---

### 5. step 与 tool_call 的区别

`step` 表示一次 LLM 决策轮次：

```python
for step in range(MAX_STEPS):
```

`tool_call` 表示模型在某一轮中申请的一次工具调用：

```python
for tool_call in tool_calls:
```

两者关系：

```text
一个 step
→ 调用一次 LLM
→ 可能包含零个、一个或多个 tool_calls
```

例如：

```text
step 0：
LLM 同时申请两个 calculator
→ 计算器执行两次

step 1：
LLM 读取两个结果并生成最终答案
```

因此：

```text
step 数量      = LLM 决策轮次
tool_call 数量 = 工具执行次数
```

---

### 6. 处理多个 tool_calls

`tool_calls` 不是数字 0 或 1，而是没有值或一个列表。

```python
tool_calls = message.get("tool_calls")
```

当它是 `None` 或空列表时：

```python
if not tool_calls:
```

条件成立，说明模型没有申请工具。

当列表中包含多个工具请求时，需要逐个处理：

```python
for tool_call in tool_calls:
    ...
```

模型返回的一条 `assistant/tool_calls` 消息只保存一次，而每一个 `tool_call` 都必须产生一条带有对应 ID 的 `role="tool"` 消息。

---

### 7. 根据 tool_name 分发工具

`if tool_calls` 用于判断模型是否申请了工具。

`tool_name` 用于判断具体申请了哪个工具。

正确层次：

```text
是否存在 tool_calls？
→ 遍历每一个 tool_call
→ 读取 tool_name
→ 验证并执行对应工具
```

当前只允许：

```python
if tool_name != "calculator":
    raise ValueError(...)
```

未来增加多个工具时，可以使用工具注册表：

```python
AVAILABLE_TOOLS = {
    "calculator": calculator,
}
```

再根据名称选择具体函数。

---

### 8. 将工具错误作为观察结果

工具执行可能失败，例如：

- 参数 JSON 不合法；
- 缺少必填参数；
- 参数类型错误；
- 工具名称未知；
- 除数为零。

程序捕获：

```python
json.JSONDecodeError
KeyError
TypeError
ValueError
```

然后将错误写入工具结果：

```python
result = f"工具调用失败: {error}"
```

这样错误不会直接破坏消息链，而是作为观察结果返回给 LLM。

测试：

```text
用户：请计算 10 ÷ 0
工具：工具调用失败，除数不能为零
LLM：解释为什么除数不能为零
```

理解到：

> Agent 的观察结果既可以是成功数据，也可以是错误信息；模型可以根据错误调整下一步或向用户解释。

---

### 9. 最大决策轮次

使用：

```python
MAX_STEPS = 5
```

限制一次用户任务最多进行五轮 LLM 决策。

作用包括：

- 防止 Agent Loop 死循环；
- 防止重复调用 LLM；
- 控制 Token 消耗和 API 费用；
- 限制运行时间；
- 避免工具之间反复触发。

超过限制时：

```python
raise RuntimeError("超过最大 Agent 决策轮次")
```

理解到：

> Agent 可以自主循环，但必须有明确的安全刹车。

---

### 10. 最大工具调用次数

使用局部计数器：

```python
tool_call_count = 0
MAX_TOOL_CALLS = 10
```

每执行一个工具请求：

```python
tool_call_count += 1
```

这限制的是一次 `run()` 中的工具调用总数，而不是整个聊天会话的累计次数。

区分：

```text
MAX_STEPS
→ 限制 LLM 决策轮次

MAX_TOOL_CALLS
→ 限制单个用户任务的工具执行总数
```

---

### 11. 失败恢复与消息清理

`main()` 捕获：

- 网络请求异常；
- Agent 超过安全限制产生的 `RuntimeError`。

任务异常结束后清空：

```python
agent.messages.clear()
```

原因是失败任务可能留下未闭合的消息链。继续发送这些历史可能导致模型处理之前的失败任务，或使 API 返回消息格式错误。

测试中将最大步数临时改为一轮，成功验证了：

```text
任务超过最大步数
→ 捕获 RuntimeError
→ 清空错误历史
→ 程序继续接收新问题
```

测试后恢复：

```python
MAX_STEPS = 5
```

---

## 今日测试结果

### 普通对话

模型直接生成答案，不调用计算器。

### 正常计算

模型申请计算器，Python 执行工具，模型根据结果生成最终回答；后续普通对话不会继续错误调用计算器。

### 除数为零

工具错误被返回给模型，模型正确解释除数不能为零，程序没有崩溃。

### 最大步数

程序能够在超过最大决策轮次时停止任务、清空错误历史，并继续下一轮聊天。

---

## 今日最大收获

今天真正完成了一个简化版工具型 Agent Loop：

```text
用户提出任务
→ LLM 决策
→ Python 执行工具
→ 工具结果返回 LLM
→ LLM 继续决策或生成最终答案
```

同时理解了 Agent 系统不能只有自主能力，还必须具备：

- 工具白名单；
- 参数和执行错误处理；
- 最大决策轮次；
- 最大工具调用次数；
- 失败后的状态恢复。

---

## 下一步计划

- 使用工具注册表管理多个工具；
- 将工具执行逻辑从 `run()` 中提取出来；
- 增加新的工具并实现动态分发；
- 完善消息回滚，避免失败时清空全部长期对话；
- 增加日志记录和更清晰的调试信息；
- 为计算器和 Agent Loop 编写自动化测试。
