import json

import pytest
from agent_with_executor import Agent


def test_agent_rejects_missing_tool_call_id(monkeypatch):
    agent = Agent("test-api-key")

    malformed_message = {
        "role": "assistant",
        "content": None,
        "tool_calls": [
            {
                "type": "function",
                "function": {
                    "name": "calculator",
                    "arguments": (
                        '{"num1": 3, "num2": 4, '
                        '"operation": "multiply"}'
                    ),
                },
            }
        ],
    }

    monkeypatch.setattr(
        agent,
        "call_llm",
        lambda: malformed_message,
    )

    with pytest.raises(
        RuntimeError,
        match="tool_call_id",
    ):
        agent.run("请计算 3 × 4")


def test_agent_returns_invalid_json_error_to_llm(monkeypatch):
    agent = Agent("test-api-key")

    responses = iter([
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "call_test",
                    "type": "function",
                    "function": {
                        "name": "calculator",
                        "arguments": "not-json",
                    },
                }
            ],
        },
        {
            "role": "assistant",
            "content": "工具参数格式错误。",
        },
    ])

    monkeypatch.setattr(
        agent,
        "call_llm",
        lambda: next(responses),
    )

    answer = agent.run("请计算 3 × 4")

    assert answer == "工具参数格式错误。"

    tool_message = agent.messages[-2]
    tool_result = json.loads(tool_message["content"])

    assert tool_message["role"] == "tool"
    assert tool_message["tool_call_id"] == "call_test"
    assert tool_result["success"] is False
    assert tool_result["error_type"] == "JSONDecodeError"