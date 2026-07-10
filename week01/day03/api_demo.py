import requests
response = requests.get("https://httpbin.org/get")

# print(response)

print(type(response))
print(type(response.text))
# print(response.text)  # just a string

data = response.json()  # convert to a Python dictionary
# print(type(response.json()))
print(type(data))
print(data.keys())
