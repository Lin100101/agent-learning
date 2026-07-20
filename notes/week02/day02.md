# Week02 Day02 - 函数对象与工具注册表

**日期：** 2026-07-20

## 今日目标

理解函数也是 Python 对象，可以被变量引用并存入字典；实现工具注册表，并让 Agent 根据模型返回的工具名称动态取得和执行函数。

---

## 今日学习内容

### 1. 函数也是对象

定义：

```python
def greet(name):
    return f"Hello, {name}!"
```

其中：

```python
greet
```

表示函数对象本身。

```python
greet("小明")
```

表示调用函数，并取得函数的返回值。

通过：

```python
print(type(greet))
```

可以看到函数对象的类型是：

```text
<class 'function'>
```

---

### 2. 函数可以赋值给变量

```python
another_greet = greet
```

此时 `another_greet` 和 `greet` 引用同一个函数对象，两者都可以调用。

而：

```python
another_greet = greet("小明")
```

会先执行函数，再把返回的字符串保存到变量中。

理解到：

```text
没有括号
→ 引用函数对象

带有括号
→ 调用函数
```

---

### 3. 将函数存入字典

实现：

```python
AVAILABLE_FUNCTIONS = {
    "add": add,
    "multiply": multiply,
}
```

字典结构：

```text
键
→ 字符串形式的函数名称

值
→ 真实的函数对象
```

根据字符串查找：

```python
selected_function = AVAILABLE_FUNCTIONS.get(function_name)
```

当键存在时，返回对应的函数对象；当键不存在时，`.get()` 返回 `None`。

---

### 4. `.get()` 与 `[]`

直接访问：

```python
AVAILABLE_FUNCTIONS["divide"]
```

键不存在时会抛出 `KeyError`。

使用：

```python
AVAILABLE_FUNCTIONS.get("divide")
```

键不存在时返回 `None`，程序可以主动处理：

```python
if selected_function is None:
    raise ValueError("未知函数")
```

---

### 5. 工具注册表

创建：

```python
AVAILABLE_TOOLS = {
    "calculator": calculator,
}
```

并封装：

```python
def get_tool(tool_name):
    tool_function = AVAILABLE_TOOLS.get(tool_name)

    if tool_function is None:
        raise ValueError(f"未知工具: {tool_name}")

    return tool_function
```

当前流程：

```text
工具名称字符串
→ get_tool()
→ AVAILABLE_TOOLS 查找
→ 返回函数对象或抛出异常
```

---

### 6. 字典解包

模型参数解析后是字典：

```python
arguments = {
    "num1": 12,
    "num2": 3,
    "operation": "multiply",
}
```

执行：

```python
tool_function(**arguments)
```

等价于：

```python
tool_function(
    num1=12,
    num2=3,
    operation="multiply",
)
```

`**` 的标准术语是字典解包或关键字参数解包。

字典键必须与函数形参名称对应，否则会产生 `TypeError`。

---

### 7. 将注册表接入 Agent

创建：

```text
agent_with_registry.py
```

Agent 不再直接定义和调用计算器，而是导入：

```python
from registry import get_tool
```

工具执行逻辑由：

```python
if tool_name != "calculator":
    ...

result = calculator(...)
```

改为：

```python
tool_function = get_tool(tool_name)
arguments = json.loads(function["arguments"])
result = tool_function(**arguments)
```

完整流程：

```text
LLM 返回 tool_name
→ 注册表取得函数对象
→ JSON 参数解析为字典
→ 字典解包为关键字参数
→ Python 执行工具函数
```

测试中成功计算：

```text
123 × 456 = 56,088
```

---

## 解耦进度

目前已经拆出：

```text
calculator.py
→ 工具实现

registry.py
→ 工具名称到函数对象的映射

agent_with_registry.py
→ Agent Loop 和模型通信
```

Agent 已不再直接调用 `calculator()`，增加新工具时不需要继续添加大量 `if/elif`。

当前仍未完全解耦：

```python
TOOLS = [...]
```

工具 JSON Schema 仍然保存在 Agent 文件中，因此 Agent 仍通过 Schema 直接知道 `calculator` 的存在。

---

## 今日最大收获

今天理解了函数不仅能被调用，也可以像其他对象一样：

- 赋值给变量；
- 存入字典；
- 作为返回值；
- 在运行时动态选择和调用。

工具注册表将：

```text
字符串工具名
```

映射为：

```text
真实 Python 函数
```

这使 Agent 的工具执行逻辑开始具备可扩展性。

---

## 下一步计划

- 实现第二个工具 `text_statistics`；
- 为第二个工具编写 JSON Schema；
- 将新工具加入注册表；
- 验证 Agent 能根据任务选择不同工具；
- 进一步整理工具函数、执行注册表和 Schema 的关系。
