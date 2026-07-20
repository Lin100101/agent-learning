import json
import os

import requests
from registry import get_tool

URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-v4-pro"

MAX_STEPS = 5
MAX_TOOL_CALLS = 10



TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "对两个数字执行基本的数学运算（加、减、乘、除）",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {
                        "type": "number",
                        "description": "第一个数字"
                    },
                    "num2": {
                        "type": "number",
                        "description": "第二个数字"
                    },
                    "operation": {
                        "type": "string",
                        "description": "需要执行的运算",
                        "enum": ["add", "subtract", "multiply", "divide"]
                    },
                },
                "required": ["num1", "num2", "operation"]
            },
        },
    }
]


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

                try:
                    tool_function = get_tool(tool_name)
                    arguments = json.loads(function["arguments"])

                    result = tool_function(**arguments)
                except (
                    json.JSONDecodeError,
                    KeyError,
                    ValueError,
                    TypeError,
                ) as error:
                    result = f"工具调用失败: {error}"

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": str(result)
                })

        raise RuntimeError("超过最大 Agent 决策轮次, 未能获得最终答案。")
    
def main():
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
