import inspect
import json
from typing import Callable, get_type_hints, Any

from pydantic import TypeAdapter


def function_to_schema(
        tool_function: Callable[..., Any]
    ) -> dict[str, Any]:
    signature = inspect.signature(tool_function)
    type_hints = get_type_hints(tool_function)

    properties = {}
    required = []

    schema = {
        "type": "function",
        "function": {
            "name": tool_function.__name__,
            "description": inspect.getdoc(tool_function) or "",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False
            },
        },
    }

    for parameter_name, parameter in signature.parameters.items():
        expected_type = type_hints[parameter_name]
        parameter_schema = TypeAdapter(expected_type).json_schema()
        is_required = parameter.default is inspect.Parameter.empty

        properties[parameter_name] = parameter_schema
        if is_required:
            required.append(parameter_name)


    return schema

if __name__ == "__main__":
    from calculator import calculator
    from text_statistics import text_statistics
    from base_converter import base_converter
    for tool_function in [
        calculator,
        text_statistics,
        base_converter
    ]:
        schema = function_to_schema(tool_function)
        print(json.dumps(schema, ensure_ascii=False, indent=2))