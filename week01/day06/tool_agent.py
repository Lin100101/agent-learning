import json
import os

import requests

URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-v4-pro"


def calculator(num1, num2, operation):
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 == 0:
            raise ValueError("Cannot divide by zero.")
        return num1 / num2
    raise ValueError(f"Unsupported operation: {operation}")


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
    
    def run(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
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

        message = response.json()["choices"][0]["message"]
        tool_calls = message.get("tool_calls")

        if tool_calls:
            tool_call = tool_calls[0]
            function = tool_call["function"]

            tool_call_id = tool_call["id"]
            tool_name = function["name"]
            arguments = json.loads(function["arguments"])

            result = calculator(
                num1=arguments["num1"],
                num2=arguments["num2"],
                operation= arguments["operation"],
            )

            print(f"工具调用 ID: {tool_call_id}")
            print(f"工具名称: {tool_name}")
            print(f"工具参数: {arguments}")

            self.messages.append(message)

            self.messages.append({
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": str(result)
            })

            return f"计算器已执行, 结果为：{result}"
        
        
        answer = message["content"]

        self.messages.append({"role": "assistant", "content": answer})

        return answer
    
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
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
