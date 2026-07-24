import json
from typing import Any

from registry import get_tool


def execute_tool(
        tool_name: str,
        arguments: dict[str, Any],
) -> dict[str, Any]:
    try:
        tool_function = get_tool(tool_name)
        result = tool_function(**arguments)

        return {
            "success": True,
            "result": result,
        }
    except (KeyError, ValueError, TypeError) as error:
        return {
            "success": False,
            "error_type": type(error).__name__,
            "error_message": str(error),
        }


if __name__ == "__main__":
    result = execute_tool(
        "calculator",
        {
            "num1": True,
            "num2": 5,
            "operation": "multiply",
        }
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))