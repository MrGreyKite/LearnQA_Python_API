import allure
import requests

from lib.logger import Logger


class MyRequests:
    @staticmethod
    @allure.step("POST request on url: {url} with data {data}")
    def post(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "POST")

    @staticmethod
    @allure.step("GET request on url: {url} with data {data}")
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "GET")

    @staticmethod
    @allure.step("PUT request on url: {url} with data {data}")
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "PUT")

    @staticmethod
    @allure.step("DELETE request on url: {url} with data {data}")
    def delete(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "DELETE")

    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str):
        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        Logger.add_request_info(url, data, headers, cookies, method)

        if method is "GET":
            response = requests.get(url=url, params=data, headers=headers, cookies=cookies, verify=False)
        elif method is "POST":
            response = requests.post(url=url, data=data, headers=headers, cookies=cookies, verify=False)
        elif method is "PUT":
            response = requests.put(url=url, data=data, headers=headers, cookies=cookies, verify=False)
        elif method is "DELETE":
            response = requests.delete(url=url, data=data, headers=headers, cookies=cookies, verify=False)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        Logger.add_response_info(response)
        allure.attach(response.text, "Server response is: ", allure.attachment_type.TEXT)

        return response
