from registry import AVAILABLE_TOOLS
from schema_generator import function_to_schema


TOOLS = [
    function_to_schema(tool_function)
    for tool_function in AVAILABLE_TOOLS.values()
]