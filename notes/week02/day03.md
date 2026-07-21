# Week02 Day03 - 多工具 Agent 与配置一致性检查

**日期：** 2026-07-21

## 今日目标

将单工具 Agent 扩展为多工具 Agent，使模型能够在计算器、文本统计和进制转换工具之间动态选择，并完成具有前后依赖关系的连续工具调用；进一步拆分工具 Schema，并在 Agent 启动时检查 Schema 与执行注册表是否一致。

---

## 今日学习内容

### 1. 文本统计工具

实现：

```python
def text_statistics(text: str, operation: str) -> int:
```

支持：

- `character_count`：统计全部字符；
- `word_count`：统计单词数量；
- `line_count`：统计行数；
- `non_whitespace_count`：统计非空白字符数量。

非空白字符统计使用：

```python
sum(1 for character in text if not character.isspace())
```

`isspace()` 比连续使用 `replace()` 更完整，可以识别空格、换行、制表符等不同空白字符。

未知操作通过 `ValueError` 拒绝执行。

---

### 2. 进制转换工具

实现：

```python
def base_converter(
    value: str,
    from_base: int,
    to_base: int,
) -> str:
```

支持二、八、十、十六进制之间的转换。

转换分为两步：

```text
原始数字字符串
→ int(value, from_base) 转为十进制中间值
→ format(decimal_value, format_code) 转为目标进制
```

格式映射：

```python
BASE_FORMATS = {
    2: "b",
    8: "o",
    10: "d",
    16: "X",
}
```

非法数字与不支持的进制都会抛出 `ValueError`。使用：

```python
raise ValueError("友好错误信息") from error
```

可以在保留原始异常原因的同时，提供更容易理解的业务错误。

---

### 3. 多工具注册表

注册表扩展为：

```python
AVAILABLE_TOOLS = {
    "calculator": calculator,
    "text_statistics": text_statistics,
    "base_converter": base_converter,
}
```

Agent 根据模型返回的工具名动态取得函数：

```text
tool_name
→ get_tool(tool_name)
→ 获得函数对象
→ tool_function(**arguments)
```

新增工具时不需要继续增加大量 `if/elif`。

---

### 4. 工具 Schema

为三个工具分别提供 JSON Schema。Schema 告诉 LLM：

- 工具名称；
- 工具用途；
- 参数名称和类型；
- 必需参数；
- `enum` 允许的参数值。

例如进制范围：

```python
"enum": [2, 8, 10, 16]
```

Schema 中的 `enum` 用于约束模型生成参数，Python 函数内部的检查用于运行时安全。两层检查不能互相替代。

---

### 5. `TOOLS` 与 `AVAILABLE_TOOLS`

二者服务于不同对象：

```text
TOOLS
→ 发送给 LLM
→ 告诉模型可以选择哪些工具

AVAILABLE_TOOLS
→ 供 Python 执行器使用
→ 根据字符串名称找到真实函数
```

如果只有 Schema，没有注册函数，LLM 可能请求一个 Python 无法执行的工具。

如果只有注册函数，没有 Schema，Python 虽然能执行，但 LLM 不知道该工具存在，因而不会主动选择它。

---

### 6. 多步、多工具 Agent

成功完成：

```text
计算 12345 × 789
→ 将结果转换成十六进制
```

执行轨迹：

```text
Agent 决策轮次 1
→ calculator
→ 9740205

Agent 决策轮次 2
→ base_converter
→ 949FAD

Agent 决策轮次 3
→ 最终回答
```

本次任务中：

- LLM 调用了 3 次；
- 工具执行了 2 次；
- 使用了 2 种不同工具。

Agent 决策轮次统计的是 LLM 请求次数，工具调用次数统计的是实际执行工具的次数，两者不是同一个概念。

---

### 7. 基础 Trace

增加运行日志：

```text
Agent 决策轮次
工具调用 ID
工具名称
工具参数
工具结果
```

最终答案正确并不能证明工具真实执行。Trace 可以确认模型选择了哪个工具、使用了什么参数，以及工具返回了什么结果。

这也是后续 Agent 运行追踪与评测项目的基础。

---

### 8. Schema 模块拆分

将工具 Schema 从 Agent 文件移动到：

```text
tool_schemas.py
```

当前结构：

```text
工具实现层
├── calculator.py
├── text_statistics.py
└── base_converter.py

工具描述与执行层
├── tool_schemas.py
├── registry.py
└── schema_registry_check.py

Agent 编排层
└── agent_with_multiple_tools.py
```

模块拆分只改变代码结构，不应改变运行行为。

---

### 9. Schema 与注册表一致性检查

使用集合差集检查：

```python
missing_in_registry = schema_tool_names - registered_tool_names
missing_in_schema = registered_tool_names - schema_tool_names
```

可以发现：

- LLM 知道但 Python 未注册的工具；
- Python 已注册但 LLM 不知道的工具。

检测到错误时，先打印具体差异，再抛出 `RuntimeError`，让自动化程序得到失败状态。

---

### 10. Fail Fast

Agent 在发送 API 请求之前执行：

```python
validate_tool_configuration()
```

流程：

```text
启动 Agent
→ 检查 Schema 与注册表
├── 不一致：立即停止
└── 一致：继续读取 API Key 并启动
```

这样可以更早暴露配置错误，避免无意义的 LLM 请求和 Token 消耗。

---

## 今日成果

- 实现 `text_statistics`；
- 实现 `base_converter`；
- 建立包含三个工具的执行注册表；
- 为三个工具编写 Schema；
- 实现依赖前一步结果的连续工具调用；
- 增加 Agent 决策轮次和工具 Trace；
- 将 Schema 拆分到独立模块；
- 实现 Schema 与注册表双向一致性检查；
- 将配置检查接入 Agent 启动流程。

---

## 下一步计划

- 统一函数类型注解；
- 学习类型注解与运行时类型检查的区别；
- 使用 Pydantic 或自定义逻辑验证工具参数；
- 让参数错误以结构化方式返回；
- 为后续自动生成 Schema 做准备。
