from calculator import calculator
from text_statistics import text_statistics
from base_converter import base_converter
from pydantic import ConfigDict, validate_call

STRICT_TOOL_CONFIG = ConfigDict(strict=True)


def build_validated_tool(tool_function):
    return validate_call(
        config=STRICT_TOOL_CONFIG,
        validate_return=True,
    )(tool_function)

AVAILABLE_TOOLS = {
    "calculator": build_validated_tool(calculator),
    "text_statistics": build_validated_tool(text_statistics),
    "base_converter": build_validated_tool(base_converter),
}

def get_tool(tool_name):
    if tool_name is None:
        raise ValueError("工具名称不能为空。")
    tool_function = AVAILABLE_TOOLS.get(tool_name)
    if tool_function is None:
        raise ValueError(f"未知工具: {tool_name}")
    
    return tool_function