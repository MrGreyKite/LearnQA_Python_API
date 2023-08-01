import pytest
import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserAuth(BaseCase):
    url_login = f"{BaseCase.base_url}/api/user/login"
    url_check_auth = f"{BaseCase.base_url}/api/user/auth"

    exclude_params = [
        "no_cookie",
        "no_token"
    ]

    def setup_method(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response_for_auth = requests.post(url=self.url_login, data=data)

        self.user_id = self.get_json_value(response_for_auth, "user_id")
        self.auth_sid = self.get_cookie(response_for_auth, "auth_sid")
        self.csrf_token = self.get_header(response_for_auth, "x-csrf-token")

    def test_auth_user(self, url_check_auth=url_check_auth):
        response_for_check_auth = requests.get(url=url_check_auth,
                                               headers={"x-csrf-token": self.csrf_token},
                                               cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(response_for_check_auth,
                                             "user_id",
                                             self.user_id,
                                             f"UserID in check method is not equal to expected userID '{self.user_id}'"
                                             )

    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth(self, condition, url_check_auth=url_check_auth):

        if condition == "no_cookie":
            response_for_check_auth = requests.get(url=url_check_auth,
                                                   cookies={"auth_sid": self.auth_sid})
        elif condition == "no_token":
            response_for_check_auth = requests.get(url=url_check_auth,
                                                   headers={"x-csrf-token": self.csrf_token})
        else:
            pytest.fail(f"No condition matched for condition '{condition}'")

        Assertions.assert_json_value_by_name(response_for_check_auth,
                                             "user_id",
                                             0,
                                             f"User is incorrectly authorized with condition '{condition}'"
                                             )
