from registry import get_tool

calculator_tool = get_tool("calculator")
text_tool = get_tool("text_statistics")
converter_tool = get_tool("base_converter")


print(calculator_tool(num1=12, num2=3, operation="multiply"))
print(text_tool("Hello Python Agent", "word_count"))
print(converter_tool("100", 10, 2))

try:
    unknown_tool = get_tool("weather")
except ValueError as error:
    print(f"测试通过, 捕获异常: {error}")