import requests
from json.decoder import JSONDecodeError

response = requests.get("https://playground.learnqa.ru/api/get_text")
print("First response is: " + response.text)

payload = {"name": "SuperMe"}
response2 = requests.get("https://playground.learnqa.ru/api/hello", params=payload)

print("Second response is: " + response2.text)

try:
    parsed_response_text = response.json()
    print(parsed_response_text)
except JSONDecodeError:
    print("Response is not JSON")
