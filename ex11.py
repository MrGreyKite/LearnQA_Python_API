import requests
import pytest


def test_cookie_value():
    # GET-запрос на указанный метод
    response_for_cookie = requests.get("https://playground.learnqa.ru/api/homework_cookie")

    print(response_for_cookie.cookies)
    print(response_for_cookie.cookies.keys())

    # Сохранение имени единственной куки в переменную
    cookie_name = list(response_for_cookie.cookies.keys())[0]
    print("Имя куки:", cookie_name)

    assert cookie_name == "HomeWork", f"There is no such cookie in response"

    cookie_value = response_for_cookie.cookies[cookie_name]
    print("Значение куки:", cookie_value)

    assert cookie_value == "hw_value", f"Cookie have an incorrect value"
