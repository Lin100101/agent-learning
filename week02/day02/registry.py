from calculator import calculator

AVAILABLE_TOOLS = {
    "calculator": calculator
}

def get_tool(tool_name):
    if tool_name is None:
        raise ValueError("工具名称不能为空。")
    tool_function = AVAILABLE_TOOLS.get(tool_name)
    if tool_function is None:
        raise ValueError(f"未知工具: {tool_name}")
    
    return tool_function