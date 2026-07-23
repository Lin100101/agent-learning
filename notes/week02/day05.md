# Week02 Day05 - 自动生成 Tool Schema

**日期：** 2026-07-23

## 今日目标

根据 Python 工具函数的名称、Docstring 和类型注解自动生成 Tool Schema，消除函数实现与手写 Schema 的双份维护。

## 原有问题

Day03、Day04 同时维护：

```text
工具函数
tool_schemas.py
```

修改函数参数后如果忘记更新手写 Schema，就会产生配置漂移。

Day05 将函数自身作为 Schema 信息来源：

```text
函数名称、Docstring、类型注解
→ function_to_schema()
→ 自动 Tool Schema
```

## 核心知识

### 1. Docstring 提供工具描述

```python
def calculator(...):
    """执行两个数字的加、减、乘、除运算。"""
```

生成器通过：

```python
inspect.getdoc(tool_function)
```

取得清理过缩进的函数说明，并写入 Schema 的 `description`。

### 2. `Literal` 表示有限取值

```python
operation: Literal[
    "add",
    "subtract",
    "multiply",
    "divide",
]
```

同一份 `Literal` 注解服务于两个消费者：

```text
Pydantic
→ 运行时只允许列出的值

TypeAdapter
→ 自动生成 JSON Schema 的 enum
```

因此不再需要分别维护验证规则和 Schema 枚举。

### 3. `TypeAdapter` 生成参数 Schema

```python
parameter_schema = TypeAdapter(
    expected_type
).json_schema()
```

示例转换：

```text
str
→ {"type": "string"}

int | float
→ anyOf: integer 或 number

Literal[2, 8, 10, 16]
→ integer + enum
```

`TypeAdapter` 在这里充当 Python 类型系统与 JSON Schema 之间的转换器。

### 4. 判断必需参数

```python
parameter.default is inspect.Parameter.empty
```

- 没有默认值：加入 `required`；
- 有默认值：不加入 `required`。

### 5. `function_to_schema()`

生成器的主要步骤：

```text
inspect.signature()
→ 取得函数参数和默认值

get_type_hints()
→ 取得解析后的类型注解

TypeAdapter(...).json_schema()
→ 生成每个参数的 JSON Schema

inspect.getdoc()
→ 取得工具说明

组合 name、description、properties、required
→ 返回完整 Tool Schema
```

生成的参数对象还包含：

```python
"additionalProperties": False
```

用于声明不允许模型生成 Schema 之外的额外参数。

### 6. 从注册表批量生成

```python
TOOLS = [
    function_to_schema(tool_function)
    for tool_function in AVAILABLE_TOOLS.values()
]
```

三个已注册工具自动生成：

- `calculator`
- `text_statistics`
- `base_converter`

Schema 在程序导入 `generated_tool_schemas` 时生成一次，不是在每次 LLM 决策时重新生成。修改函数后需要重新启动进程。

### 7. 一致性检查仍有价值

Schema 虽然根据注册函数自动生成，但注册表键名仍可能写错：

```python
"calculator_typo": build_validated_tool(calculator)
```

此时：

```text
注册表名称：calculator_typo
Schema 名称：calculator
```

`schema_registry_check.py` 可以继续发现这类名称不一致。

## 最终调用结构

```text
Python 工具函数
├── __name__
├── Docstring
├── 类型注解
└── Literal
        ↓
registry.py
├── 注册工具
└── Pydantic 严格验证包装
        ↓
generated_tool_schemas.py
└── function_to_schema() 自动生成 TOOLS
        ↓
Agent
├── 把 TOOLS 发送给 LLM
└── 通过 get_tool() 执行验证后的函数
```

## 实际验收

自动 Schema 成功完成：

```text
统计 “Hello Python Agent” 的非空白字符数
→ text_statistics
→ 16
```

以及连续工具调用：

```text
123 × 456
→ calculator
→ 56088
→ base_converter
→ DB18
```

Agent 共进行三次决策，执行两次工具，最终答案正确。

## 今日成果

- 为三个工具增加 Docstring；
- 使用 `Literal` 表达工具参数枚举；
- 使用 `TypeAdapter` 将类型注解转换为 JSON Schema；
- 实现通用 `function_to_schema()`；
- 从工具注册表自动生成完整 `TOOLS`；
- 将真实 Agent 切换到自动 Schema；
- 删除 Day05 中不再使用的手写 `tool_schemas.py`；
- 保留注册表键名与生成 Schema 名称的一致性检查；
- 验证单工具和连续多工具调用均正常。

