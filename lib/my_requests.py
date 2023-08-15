import requests

from lib.logger import Logger


class MyRequests:
    @staticmethod
    def post(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "POST")

    @staticmethod
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "GET")

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "PUT")

    @staticmethod
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

        return response
