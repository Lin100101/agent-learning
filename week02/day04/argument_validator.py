import inspect
from typing import Any, Callable, get_type_hints, get_args


def _matches_expected_type(
    value: Any,
    expected_type: Any
) -> bool:
    if expected_type is Any:
        return True
    
    if isinstance(value, bool):
        allowed_types = get_args(expected_type) or (expected_type,)
        return bool in allowed_types
    return isinstance(value, expected_type)


def validate_tool_arguments(
        tool_function: Callable[..., Any],
        arguments: dict[str, Any],
) -> dict[str, Any]:
    signature = inspect.signature(tool_function)
    try:
        bound_arguments = signature.bind(**arguments)
    except TypeError as error:
        raise TypeError(f"工具参数结构错误: {error}") from error
    
    bound_arguments.apply_defaults()
    type_hints = get_type_hints(tool_function)
    for parameter_name, value in bound_arguments.arguments.items():
        expected_type = type_hints.get(parameter_name)
        if expected_type is None:
            continue
        if not _matches_expected_type(value, expected_type):
            raise TypeError(
                f"参数 '{parameter_name}' 类型错误: "
                f"期望类型 {expected_type}, 实际类型 {type(value)}"
            )
    return bound_arguments.arguments




def multiply(num1: int, num2: int = 2) -> int:
    return num1 * num2

def ping() -> str:
    return "pong"

def set_enabled(enabled: bool) -> bool:
    return enabled


if __name__ == "__main__":
    print(
        validate_tool_arguments(
            multiply,
            {"num1": 3, "num2": 4}
        )
    )
    print(
        validate_tool_arguments(
            ping,
            {}
        )
    )


    print(
        validate_tool_arguments(
            set_enabled,
            {
                "enabled": True,
            }
        )
    )
