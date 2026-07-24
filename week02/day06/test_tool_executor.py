import pytest
from tool_executor import execute_tool


def test_execute_tool_success():
    result = execute_tool(
        "calculator",
        {
            "num1": 3,
            "num2": 4,
            "operation": "multiply",
        },
    )

    assert result["success"] is True
    assert result["result"] == 12


def test_execute_tool_business_error():
    result = execute_tool(
        "calculator",
        {
            "num1": 10,
            "num2": 0,
            "operation": "divide",
        },
    )

    assert result["success"] is False
    assert result["error_type"] == "ValueError"
    assert result["error_message"] == "除数不能为零。"


def test_execute_tool_validation_error():
    result = execute_tool(
        "calculator",
        {
            "num1": True,
            "num2": 4,
            "operation": "multiply",
        },
    )

    assert result["success"] is False
    assert result["error_type"] == "ValidationError"
    assert "num1" in result["error_message"]


def test_execute_tool_unknown_tool():
    result = execute_tool(
        "unknown_tool",
        {},
    )

    assert result["success"] is False
    assert result["error_type"] == "ValueError"
    assert "未知工具" in result["error_message"]


@pytest.mark.parametrize(
    ("tool_name", "arguments", "expected_result"),
    [
        (
            "text_statistics",
            {
                "text": "Hello Python Agent",
                "operation": "non_whitespace_count",
            },
            16,
        ),
        (
            "base_converter",
            {
                "value": "50",
                "from_base": 10,
                "to_base": 2,
            },
            "110010",
        ),
    ],
)
def test_execute_other_tools_success(
    tool_name,
    arguments,
    expected_result,
):
    result = execute_tool(tool_name, arguments)

    assert result["success"] is True
    assert result["result"] == expected_result