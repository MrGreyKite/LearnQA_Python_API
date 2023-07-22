import requests

response_with_redirect = requests.get("https://playground.learnqa.ru/api/long_redirect")

history_arr = response_with_redirect.history
print(f"Количество редиректов до итогового урла: {len(history_arr)}")

last_element_of_history = history_arr[-1].url
print(f"Второй редирект на {last_element_of_history}")

print(f"Итоговый урл после всех редиректов: {response_with_redirect.url}")

