import requests


url = "https://api.deepseek.com/chat/completions"

header = {
    "Authorization": "Bearer sk-363a8208f38d48aea2b27afc65082119",
    "content-type": "application/json"
}

data = {
    "model": "deepseek-v4-pro",
    "messages": [
        {
            "role": "user",
            "content": "你好。"
        }
    ]
}

response = requests.post(url, headers=header, json=data)

print(response.status_code)
print(response.json()["choices"][0]["message"]["content"])