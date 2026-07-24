# Week02 Day06 - 独立工具执行器与自动化测试

**日期：** 2026-07-24

## 今日目标

将工具查找、执行和错误包装从 Agent Loop 中拆分为独立执行器，并使用 pytest 为执行层和工具调用协议层建立自动化测试。

---

## 一、为什么拆分工具执行器

拆分前，`Agent.run()` 同时负责：

```text
调用 LLM
解析 tool_calls
查找工具
执行工具
处理工具异常
包装工具结果
维护 messages
```

职责过多会带来两个问题：

- Agent Loop 难以阅读和维护；
- 测试工具执行时必须经过 LLM，速度慢、结果不稳定且消耗 Token。

拆分后：

```text
Agent
├── 调用 LLM
├── 解析工具调用协议
├── 调用 execute_tool()
└── 维护 messages

Tool Executor
├── 从注册表查找工具
├── 执行工具
├── 捕获工具异常
└── 返回统一结构
```

---

## 二、独立工具执行器

核心接口：

```python
def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
```

成功结果：

```python
{
    "success": True,
    "result": result,
}
```

失败结果：

```python
{
    "success": False,
    "error_type": type(error).__name__,
    "error_message": str(error),
}
```

执行器处理：

- 未知工具；
- Pydantic 参数验证失败；
- 工具内部业务异常；
- 调用参数结构错误。

### 为什么执行器不处理 `json.loads()`

LLM 返回的 `function["arguments"]` 是 JSON 字符串，属于模型接口协议。

```text
LLM arguments 字符串
→ Agent 使用 json.loads() 解析
→ 得到 Python dict
→ Executor 接收 dict 并执行工具
```

这样执行器不依赖具体 LLM API，可以被命令行、FastAPI、测试代码或其他 Agent 复用。

---

## 三、异常类型

### `ValueError`

`ValueError` 不只表示数值计算错误，而是广义的“值不符合当前业务要求”。

当前项目中的例子：

- 除数不能为零；
- 未知工具名称；
- 不支持的操作；
- 非法进制内容。

### Pydantic `ValidationError`

表示输入参数或函数返回值不符合类型注解和 Pydantic 规则，例如：

- 使用 `True` 代替 `int | float`；
- 字符串不符合 `Literal` 枚举；
- `list[str]` 中出现非字符串元素；
- 返回值类型不符合声明。

`ValidationError` 属于 `ValueError` 体系，因此可以被现有 `except ValueError` 捕获，但结构化结果会保留具体类名 `ValidationError`。

---

## 四、Agent 协议异常边界

### `tool_call_id` 缺失

工具结果必须通过 `tool_call_id` 与模型请求一一对应。如果 ID 缺失，就无法构造合法的 `role="tool"` 消息。

处理方式：

```text
缺少或无效的 tool_call_id
→ 抛出 RuntimeError
→ 主程序清空不完整对话历史
```

### 其他协议字段错误

如果 ID 有效，但 `function`、`name`、`arguments` 或 JSON 格式错误，可以生成结构化失败结果：

```text
捕获协议解析异常
→ 生成 success=False
→ 使用有效 tool_call_id 写入 tool 消息
→ 让 LLM 再次决策
```

---

## 五、pytest 基础

pytest 的发现规则：

- 测试文件通常命名为 `test_*.py` 或 `*_test.py`；
- 测试函数以 `test_` 开头；
- 使用普通 `assert` 判断结果；
- 不需要 `if __name__ == "__main__":`。

示例：

```python
def test_execute_tool_success():
    result = execute_tool(...)

    assert result["success"] is True
    assert result["result"] == 12
```

断言失败时，pytest 会展示：

- 失败的测试函数；
- 失败代码行；
- 实际值；
- 期望值。

---

## 六、参数化测试

`@pytest.mark.parametrize` 让同一个测试函数使用多组输入重复运行：

```text
同一份断言逻辑
├── 第一组参数 → 独立测试结果
└── 第二组参数 → 独立测试结果
```

它解决的是重复编写相同测试逻辑的问题，不要求每组参数对应不同函数。每组参数都会生成一个独立测试用例，因此两组参数计为两条测试。

本次使用参数化测试覆盖：

- `text_statistics`
- `base_converter`

---

## 七、monkeypatch

协议测试不应真的请求 LLM。使用：

```python
monkeypatch.setattr(
    agent,
    "call_llm",
    fake_call_llm,
)
```

临时替换 Agent 实例的 `call_llm()`：

```text
Agent.run()
→ 不访问 DeepSeek
→ 返回测试准备的假响应
```

价值：

- 不需要 API Key；
- 不访问网络；
- 不消耗 Token；
- 测试结果稳定；
- 可以构造正常 API 很难稳定产生的异常响应。

使用迭代器可以模拟多次 LLM 决策：

```python
responses = iter([first_response, second_response])
lambda: next(responses)
```

---

## 八、最终测试覆盖

Day06 最终共有 8 条自动化测试：

```text
1. calculator 正常执行
2. 除零业务异常
3. Pydantic 参数验证失败
4. 未知工具
5. text_statistics 正常执行
6. base_converter 正常执行
7. 缺少 tool_call_id
8. 非法 arguments JSON 的错误恢复
```

最终结果：

```text
8 passed
```

此外，真实 Agent 回归测试通过：

- 普通计算；
- 除零错误恢复；
- calculator 与 base_converter 连续工具调用。

---

## 今日成果

- 实现独立 `execute_tool()`；
- 将 Agent Loop 接入工具执行器；
- 分离 JSON 协议解析与 Python 工具执行；
- 为执行器建立成功、业务异常、参数异常和未知工具测试；
- 使用参数化测试覆盖全部三个工具；
- 使用 monkeypatch 模拟 LLM 响应；
- 增加 `tool_call_id` 缺失保护；
- 测试非法 JSON 的结构化错误反馈；
- 将 pytest 加入开发依赖；
- 忽略 pytest、Ruff 和覆盖率缓存文件。

