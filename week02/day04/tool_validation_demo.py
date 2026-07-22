from argument_validator import validate_tool_arguments
from registry import get_tool

calculator_tool = get_tool("calculator")

arguments = validate_tool_arguments(
    calculator_tool,
    {
        "num1": 12,
        "num2": 3,
        "operation": "multiply",
    },
)

converter = get_tool("base_converter")

validated_arguments = validate_tool_arguments(
    converter,
    {
        "value": "100",
        "from_base": 10,
        "to_base": 2,
    },
)

print(arguments)
print(calculator_tool(**arguments))

print(validated_arguments)
print(converter(**validated_arguments))