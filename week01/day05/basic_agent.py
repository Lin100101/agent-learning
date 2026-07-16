import requests

URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-v4-pro"


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
            "messages": self.messages
        }
        response = requests.post(URL, headers=self.headers, json=data, timeout=60)
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": answer})
        return answer
    
def main():
    api_key = input("Please enter yourDeepSeek API Key: ").strip()
    agent = Agent(api_key)

    while True:
        user_input = input("user:")
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
