def calculator(
        num1: int | float,
        num2: int | float,
        operation: str,
    ) -> int | float:
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 == 0:
            raise ValueError("除数不能为零。")
        return num1 / num2
    raise ValueError(f"不支持的操作: {operation}")