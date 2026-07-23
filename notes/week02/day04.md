# Week02 Day04 - 工具参数验证与结构化错误反馈

**日期：** 2026-07-22

## 今日目标

理解 Python 类型注解与运行时验证的区别，为 Agent 工具增加可靠的参数、返回值和业务异常保护。

## 核心知识

### 1. 类型注解不会自动验证

```python
def add(num1: int, num2: int) -> int:
    return num1 + num2
```

类型注解主要服务于代码阅读、IDE、静态检查和框架反射。Python 默认不会因为传入字符串就自动拒绝调用，也不会自动检查返回值。

### 2. 使用 `inspect` 检查参数结构

```python
signature = inspect.signature(tool_function)
bound_arguments = signature.bind(**arguments)
bound_arguments.apply_defaults()
```

- `bind()` 检查缺少参数和多余参数；
- `apply_defaults()` 补充函数默认值；
- 它们不负责检查参数类型。

### 3. 手写类型验证器及其边界

使用 `get_type_hints()` 获取解析后的类型注解，再逐个检查参数。

需要特别注意：

- `bool` 是 `int` 的子类，`isinstance(True, int)` 为 `True`；
- `list[str]` 等参数化泛型不能直接作为 `isinstance()` 的第二个参数；
- 嵌套类型越复杂，手写递归验证器越难维护。

因此手写验证器适合理解原理，但真实工具运行时改用专业验证库。

### 4. Pydantic `validate_call`

```python
@validate_call(
    config=ConfigDict(strict=True),
    validate_return=True,
)
```

- `strict=True`：拒绝把 `"3"`、`True` 等值宽松转换为数字；
- `validate_return=True`：同时检查函数返回值；
- 支持 `list[str]`、联合类型等复合类型；
- 验证失败时抛出 `ValidationError`。

### 5. 在注册表统一包装工具

```python
def build_validated_tool(tool_function):
    return validate_call(
        config=STRICT_TOOL_CONFIG,
        validate_return=True,
    )(tool_function)
```

`AVAILABLE_TOOLS` 保存经过 Pydantic 包装的函数。Agent 只要始终通过 `get_tool()` 获取工具，就会自动经过统一验证。

模块职责：

```text
工具文件
→ 实现业务逻辑

registry.py
→ 注册工具并增加 Pydantic 验证

Agent
→ 解析调用、查找工具、执行并保存结果
```

### 6. 类型错误与业务错误

Pydantic 负责参数结构和类型，例如拒绝：

```python
calculator(num1=True, num2=4, operation="multiply")
```

工具函数负责业务规则，例如：

```text
10 ÷ 0
```

参数类型正确，所以通过 Pydantic；随后 `calculator()` 根据业务规则抛出 `ValueError`。

### 7. 结构化工具结果

成功结果：

```python
{
    "success": True,
    "result": 20,
}
```

失败结果：

```python
{
    "success": False,
    "error_type": "ValueError",
    "error_message": "除数不能为零。",
}
```

工具消息的 `content` 必须是字符串，因此使用：

```python
json.dumps(tool_result, ensure_ascii=False)
```

完整错误恢复流程：

```text
工具抛出异常
→ Python 的 except 捕获
→ 转换为结构化失败结果
→ 作为 role="tool" 写入 messages
→ LLM 决定修正参数、改用工具或解释错误
```

## 今日成果

- 理解类型注解不会自动执行运行时验证；
- 使用 `inspect.signature().bind()` 检查参数结构；
- 实现手写参数验证器；
- 认识 `bool`、联合类型和参数化泛型的验证边界；
- 引入 Pydantic 严格参数与返回值验证；
- 在工具注册表统一包装全部工具；
- 将工具成功和失败结果改为结构化数据；
- 验证工具业务异常不会导致整个 Agent 崩溃。

