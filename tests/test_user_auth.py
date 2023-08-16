import allure
import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("User Authentication cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        "no_cookie",
        "no_token"
    ]

#    @allure.step("Setup - getting auth data") - получается ошибка
    def setup_method(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response_for_auth = MyRequests.post(url=self.url_login, data=data)

        self.user_id = self.get_json_value(response_for_auth, "user_id")
        self.auth_sid = self.get_cookie(response_for_auth, "auth_sid")
        self.csrf_token = self.get_header(response_for_auth, "x-csrf-token")

    @allure.title("Checking the state of user auth with correct data")
    @allure.description("Verifying that user is logged when request has correct header and cookie")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_auth_user(self):
        response_for_check_auth = MyRequests.get(url=self.url_check_auth,
                                                 headers={"x-csrf-token": self.csrf_token},
                                                 cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(response_for_check_auth,
                                             "user_id",
                                             self.user_id,
                                             f"UserID in check method is not equal to expected userID '{self.user_id}'"
                                             )

    @allure.title("Checking the state of user auth with incomplete data - {condition}")
    @allure.description("Verifying that user is not logged when request doesn't have both correct header and cookie")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth(self, condition):

        if condition == "no_cookie":
            response_for_check_auth = MyRequests.get(url=self.url_check_auth,
                                                     cookies={"auth_sid": self.auth_sid})
        elif condition == "no_token":
            response_for_check_auth = MyRequests.get(url=self.url_check_auth,
                                                     headers={"x-csrf-token": self.csrf_token})
        else:
            pytest.fail(f"No condition matched for condition '{condition}'")

        Assertions.assert_json_value_by_name(response_for_check_auth,
                                             "user_id",
                                             0,
                                             f"User is incorrectly authorized with condition '{condition}'"
                                             )
