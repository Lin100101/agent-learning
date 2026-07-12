import requests

URL = "https://api.deepseek.com/chat/completions"

HEADERS = {
    "Authorization": "Bearer sk-xxxxxxxxxxxxx",  # Replace with your actual API key
    "content-type": "application/json"
}

MODEL = "deepseek-v4-pro"
messages = []

while True:
    question = input("你：")
    if question.lower() in ["exit", "quit"]:
        print("Exiting the chat. Goodbye!")
        break
    messages.append({"role": "user", "content": question})
    data = {
        "model": MODEL,
        "messages": messages
    }
    response = requests.post(URL, headers=HEADERS, json=data)

    if response.status_code == 200:
        answer = response.json()["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": answer})
        print(f"AI: {answer}")
    else:
        print(f"Error: {response.status_code} - {response.text}")