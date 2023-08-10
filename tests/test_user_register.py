import requests
from datetime import datetime
import random

from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    url_create_user = f"{BaseCase.base_url}/api/user"
    existing_email = "vinkotov@example.com"

    def setup_method(self):
        base_part = "learqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_new_user_successfully(self):
        data = {
            "password": "pss2",
            "username": f"Test {random.randint(0, 1000)}",
            "firstName": "Tes",
            "lastName": "Testoff",
            "email": self.email
        }

        response = requests.post(url=self.url_create_user, data=data)

        Assertions.assert_status_code_is(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_already_existing_email(self):
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": self.existing_email
        }

        response = requests.post(url=self.url_create_user, data=data)

        Assertions.assert_status_code_is(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{self.existing_email}' already exists", \
            f"Unexpected response content {response.content}"
