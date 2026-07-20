from registry import get_tool

tool_name = "calculator"

arguments = {
    "num1": 12,
    "num2": 3,
    "operation": "multiply", 
}

tool_function = get_tool(tool_name)

result = tool_function(**arguments)

print(tool_function)
print(result)