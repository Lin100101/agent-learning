def calculator(num1, num2, operation):
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 == 0:
            raise ValueError("Cannot divide by zero.")
        return num1 / num2
    raise ValueError(f"Unsupported operation: {operation}")

if __name__ == "__main__":  # 入口保护
    # 测试 calculator 函数
    test_result = calculator(10, 5, "add")
    print(f"Test Result: {test_result}")