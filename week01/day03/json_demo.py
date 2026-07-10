import json
import requests
from requests.exceptions import RequestException

try:
    response = requests.get("https://httpbin.org/get")
    response.raise_for_status()
    data = response.json()
    print(type(data))
    print(json.dumps(data, indent=4))
except RequestException as e:
    print(f"An error occurred: {e}")
except json.JSONDecodeError as e:
    print(f"JSON decoding failed: {e}")

