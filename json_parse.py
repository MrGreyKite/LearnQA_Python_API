import json

string_as_json = '{"answer": "Hello, my friend"}'
obj = json.loads(string_as_json)
print(obj['answer'])

key = "answer2"

if key in obj:
    print(obj[key])
else:
    print(f"Key {key} is not found")

