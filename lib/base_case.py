import json.decoder
from datetime import datetime
import random

import allure
from requests import Response


class BaseCase:
    base_url = "https://playground.learnqa.ru/api"

    url_create_user = f"{base_url}/user"
    url_login = f"{base_url}/user/login"
    url_check_auth = f"{base_url}/user/auth"
    url_user_by_id_pattern = f"{base_url}/user/"

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

    @allure.step("Preparing data for test user creation")
    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"

        return {
            "password": "pass2ord",
            "username": f"UserTest {random.randint(0, 1000)}",
            "firstName": "Test",
            "lastName": "Testy",
            "email": email
        }
