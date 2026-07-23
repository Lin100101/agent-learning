import json
import os

import requests
from registry import get_tool
from generated_tool_schemas import TOOLS
from schema_registry_check import validate_tool_configuration

URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-v4-pro"

MAX_STEPS = 5
MAX_TOOL_CALLS = 10



class Agent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "content-type": "application/json"
        }
        self.messages = []
    
    def call_llm(self):
        data = {
            "model": MODEL,
            "messages": self.messages,
            "tools": TOOLS,
            "tool_choice": "auto",
            "thinking": {
                "type": "disabled",
            },
        }

        response = requests.post(
            URL,
            headers=self.headers,
            json=data,
            timeout=60
        )
        response.raise_for_status()

        return response.json()["choices"][0]["message"]
    
    def run(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        
        tool_call_count = 0
    
        for step in range(MAX_STEPS):
            print(f"\nAgent 决策轮次: {step + 1}")
            message = self.call_llm()
            tool_calls = message.get("tool_calls")
            if not tool_calls:
                answer = message["content"]
                self.messages.append(message)
                return answer
            
            self.messages.append(message)

            for tool_call in tool_calls:
                tool_call_count += 1
                if tool_call_count > MAX_TOOL_CALLS:
                    raise RuntimeError("超过最大工具调用次数")

                function = tool_call["function"]

                tool_call_id = tool_call["id"]
                tool_name = function["name"]

                print(f"工具调用 ID: {tool_call_id}")
                print(f"工具名称: {tool_name}")
                print(f"工具原始参数: {function['arguments']}")


                try:
                    tool_function = get_tool(tool_name)
                    arguments = json.loads(function["arguments"])
                    result = tool_function(**arguments)
                    tool_result = {
                        "success": True,
                        "result": result,
                    }
                except (
                    json.JSONDecodeError,
                    KeyError,
                    ValueError,
                    TypeError,
                ) as error:
                    error_type = type(error).__name__
                    error_message = str(error)
                    tool_result = {
                        "success": False,
                        "error_type": error_type,
                        "error_message": error_message,
                    }

                print(f"工具结果: {tool_result}")

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": json.dumps(tool_result, ensure_ascii=False),
                })

        raise RuntimeError("超过最大 Agent 决策轮次, 未能获得最终答案。")
    
def main():
    validate_tool_configuration()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("Error: Please set the DEEPSEEK_API_KEY environment variable.")
        return
    print("API Key found. Starting the chat agent...")
    agent = Agent(api_key)

    while True:
        user_input = input("user: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat. Goodbye!")
            break
        if not user_input:
            continue
        try:
            answer = agent.run(user_input)
            print(f"AI: {answer}")
        except requests.exceptions.RequestException as error:
            print(f"RequestError: {error}")
            agent.messages.clear()
            print("请检查网络连接或 API Key 是否正确, 并重新提问。")
        except RuntimeError as error:
            print(f"Agent Error: {error}")
            agent.messages.clear()
            print("对话历史已重置, 请重新提问。")


if __name__ == "__main__":
    main()
