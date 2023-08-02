import requests
import pytest


def test_header_value():
    response_for_header = requests.get("https://playground.learnqa.ru/api/homework_header")

    headers_list = list(response_for_header.headers.items())

    print("Все заголовки:")
    for header, value in response_for_header.headers.items():
        index = headers_list.index((header, value))
        print(header, ":", value, f", место в списке {index}")

    header_name = headers_list[6][0]
    print("Имя хедера:", header_name)

    assert header_name == "x-secret-homework-header", f"There is no such header in response"

    header_value = response_for_header.headers[header_name]
    print("Значение хедера:", header_value)

    assert header_value == "Some secret value", f"Header have an incorrect value"
