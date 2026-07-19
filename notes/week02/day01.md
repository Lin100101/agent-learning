# Week02 Day01 - 函数、模块与代码拆分

**日期：** 2026-07-19

## 今日目标

复习函数的参数与返回值，理解 Python 模块的导入机制，并将 Week01 Agent 中的计算器拆分为独立模块，为后续多工具 Agent 的模块化重构打基础。

---

## 今日学习内容

### 1. 函数与模块

函数是一段具有明确输入、处理逻辑和返回值的可复用代码。

模块是一个 `.py` 文件，用于组织相关的函数、类和变量。

今天将计算器拆分为：

```text
week02/day01/
├── calculator.py
├── calculator_demo.py
└── function_demo.py
```

其中：

```text
calculator.py
→ 定义和测试计算器函数

calculator_demo.py
→ 导入并调用计算器

function_demo.py
→ 练习参数、默认值和返回值
```

---

### 2. 导入模块

学习了两种导入方式。

直接导入函数：

```python
from calculator import calculator
```

调用：

```python
calculator(...)
```

导入整个模块：

```python
import calculator
```

调用：

```python
calculator.calculator(...)
```

在 `calculator.calculator()` 中：

```text
点号左侧 calculator
→ 模块名

点号右侧 calculator
→ 模块中的函数名
```

导入整个模块时，函数来源更加明确，也能减少名称冲突。

---

### 3. 模块的顶层代码

Python 第一次导入模块时，会执行模块中的顶层代码。

函数定义：

```python
def calculator(...):
    ...
```

会创建函数对象，但函数体不会在定义时执行。只有调用函数时才会执行函数体。

普通顶层代码则会在导入模块时立即执行，例如：

```python
print("模块正在加载")
```

---

### 4. 入口保护

使用：

```python
if __name__ == "__main__":
    ...
```

控制一段代码只在文件被直接运行时执行。

```text
直接运行 calculator.py
→ __name__ == "__main__"
→ 执行测试代码

从其他文件导入 calculator.py
→ __name__ == "calculator"
→ 不执行测试代码
```

入口保护不仅可以保护测试代码，也适用于程序入口、演示代码和其他不应在导入时执行的顶层逻辑。

---

### 5. 函数与方法

模块中的独立函数：

```python
calculator.calculator(...)
requests.post(...)
os.getenv(...)
```

对象的方法：

```python
response.raise_for_status()
agent.call_llm()
```

可以辅助记忆为：

```text
模块.函数()
对象.方法()
```

方法通常定义在类中，并通过对象或类调用。

---

### 6. 形参与实参

定义函数时：

```python
def calculator(num1, num2, operation):
    ...
```

`num1`、`num2` 和 `operation` 是形参。

调用函数时：

```python
calculator(12, 3, "multiply")
```

`12`、`3` 和 `"multiply"` 是实参。

位置参数根据顺序匹配，关键字参数根据名称匹配：

```python
calculator(
    num2=3,
    operation="multiply",
    num1=12,
)
```

关键字参数在参数较多时通常更容易阅读。

---

### 7. 默认参数

实现了：

```python
def calculate_total(price, quantity, discount=0):
    ...
```

当调用者没有传入 `discount` 时，自动使用默认值 `0`。

测试结果：

```text
calculate_total(100, 2)
→ 200

calculate_total(100, 2, 0.2)
→ 160.0
```

---

### 8. return 与 print

`return` 将结果返回给调用者：

```python
result = calculate_total(...)
```

`print` 只把内容显示在终端：

```python
print(result)
```

如果函数只有 `print()` 而没有 `return`，调用者得到的返回值是 `None`。

工具函数应该主要负责计算并返回结果，终端显示由调用方负责。

---

## 今日代码实践

### 独立计算器模块

`calculator.py` 中保留计算逻辑，并使用入口保护放置测试代码。

### 模块导入

`calculator_demo.py` 使用：

```python
import calculator
```

成功调用模块中的计算器函数并得到除法结果。

### 函数参数练习

`function_demo.py` 实现商品总价与折扣计算，正确使用：

- 默认参数；
- 位置参数；
- 关键字参数；
- `return`；
- 入口保护。

---

## 今日最大收获

今天开始从“把所有代码写在一个文件中”过渡到“根据职责组织模块”。

核心认识：

```text
函数
→ 封装一项明确逻辑

模块
→ 组织相关函数和类

入口保护
→ 区分直接运行与被导入

return
→ 将计算结果交给调用者
```

拆分模块能够降低代码耦合，使工具更容易复用、测试、维护和扩展。

---

## 下一步计划

- 学习函数对象；
- 使用字典保存函数；
- 实现工具名称到函数的映射；
- 创建工具注册表；
- 使用工具注册表替代写死的工具名称判断。
