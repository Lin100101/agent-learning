def add(num1, num2):
    return num1 + num2

def multiply(num1, num2):
    return num1 * num2

AVAILABLE_FUNCTIONS = {
    "add": add,
    "multiply": multiply
}

function_name = "divide"

selected_function = AVAILABLE_FUNCTIONS.get(function_name)

if selected_function is None:
    raise ValueError(f"未知函数: {function_name}")

result = selected_function(12, 3)

print(selected_function)
print(result)