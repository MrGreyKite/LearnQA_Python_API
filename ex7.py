import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# 1. Запрос без параметра method
response = requests.get(url)
print("1. Запрос без параметра method:")
print(response.text)
print("--------")

# 2. Запрос с неподдерживаемым типом запроса (HEAD)
response = requests.head(url)
print("2. Запрос с неподдерживаемым типом запроса (HEAD):")
print(response.text)
print("--------")

# 3. Запрос с правильным значением параметра method (GET)
params = {"method": "GET"}
response = requests.get(url, params=params)
print("3. Запрос с допустимым значением параметра method (GET):")
print(response.text)
print("--------")

# 4. Проверка всех возможных сочетаний допустимых типов запроса и значений параметра method
request_types = ["GET", "POST", "PUT", "DELETE"]

print("4. Проверка сочетаний допустимых типов запроса и значений параметра method:")
for request_type in request_types:
    for method_value in request_types:
        params = {"method": method_value}
        if request_type == "GET":
            response = requests.get(url, params=params)
        else:
            data = {"method": method_value}
            response = requests.request(request_type, url, data=data)

        if (request_type != method_value and response.text == '{"success":"!"}') \
                or (request_type == method_value and response.text == ''):
            print(
                f"Ошибка: получен некорректный ответ для запроса '{request_type}' с параметром method='{method_value}'")

