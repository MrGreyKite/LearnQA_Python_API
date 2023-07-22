import requests
import time

# Шаг 1: создание задачи
response1 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job')
data1 = response1.json()
token = data1['token']
seconds_to_wait = data1['seconds']

# Шаг 2: запрос до готовности задачи
response2 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params={'token': token})
data2 = response2.json()
status = data2['status']
if status != "Job is NOT ready":
    print("Error: Unexpected status value. The job is likely already completed.")
else:
    print(f"Status of fresh job: {status}")

# Шаг 3: ожидание нужного количества секунд
time.sleep(seconds_to_wait)

# Шаг 4: запрос после готовности задачи
response3 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params={'token': token})
data3 = response3.json()

status = data3['status']
if status == "Job is ready":
    print(f"Status after waiting: {status}")
else:
    print("Error: Unexpected status value. The job might not be completed yet.")

try:
    result = data3['result']
    print(f"Result of current job is: {result}")
except KeyError:
    print("Error: Result field is missing in the JSON response.")
