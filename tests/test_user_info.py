from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserInfo(BaseCase):

    def test_get_user_info_no_auth(self):
        user_id = "2"
        response = MyRequests.get(url=self.url_user_by_id_pattern + user_id)

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_doesnt_have_key(response, "email")
        Assertions.assert_json_doesnt_have_key(response, "firstName")
        Assertions.assert_json_doesnt_have_key(response, "lastName")

    def test_get_user_info_as_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response_for_auth = MyRequests.post(url=self.url_login, data=data)

        auth_sid = self.get_cookie(response_for_auth, "auth_sid")
        csrf_token = self.get_header(response_for_auth, "x-csrf-token")
        user_id_from_auth = self.get_json_value(response_for_auth, "user_id")

        response_info = MyRequests.get(url=self.url_user_by_id_pattern + str(user_id_from_auth),
                                       headers={"x-csrf-token": csrf_token},
                                       cookies={"auth_sid": auth_sid}
                                       )
        Assertions.assert_json_has_keys(response_info, ["username", "email", "firstName", "lastName"])

    def test_get_user_info_as_another_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response_for_auth = MyRequests.post(url=self.url_login, data=data)

        auth_sid = self.get_cookie(response_for_auth, "auth_sid")
        csrf_token = self.get_header(response_for_auth, "x-csrf-token")

        response_info = MyRequests.get(url=self.url_user_by_id_pattern + "1",
                                       headers={"x-csrf-token": csrf_token},
                                       cookies={"auth_sid": auth_sid}
                                       )
        Assertions.assert_json_has_key(response_info, "username")
        Assertions.assert_json_doesnt_have_key(response_info, "email")
        Assertions.assert_json_doesnt_have_key(response_info, "firstName")
        Assertions.assert_json_doesnt_have_key(response_info, "lastName")
