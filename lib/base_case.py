import json.decoder

from requests import Response


class BaseCase:
    base_url = "https://playground.learnqa.ru"

    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cookie with name {cookie_name} is not found in response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"Header with name {header_name} is not found in response"
        return response.headers[header_name]

    def get_json_value(self, response: Response, key_name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response isn't in JSON format. Response is: '{response.text}'"
        assert key_name in response_as_dict, f"Response doesn't have a key '{key_name}'"
        return response_as_dict[key_name]
