from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def test_default_user_delete(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response_for_auth = MyRequests.post(url=self.url_login, data=data)

        self.user_id = self.get_json_value(response_for_auth, "user_id")
        self.auth_sid = self.get_cookie(response_for_auth, "auth_sid")
        self.csrf_token = self.get_header(response_for_auth, "x-csrf-token")

        response = MyRequests.delete(url=self.url_user_by_id_pattern + str(self.user_id),
                                     headers={"x-csrf-token": self.csrf_token},
                                     cookies={"auth_sid": self.auth_sid}
                                     )
        Assertions.assert_status_code_is(response, 400)
        assert response.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5."

    def test_delete_user_successful(self):
        register_data = self.prepare_registration_data()
        response_user = MyRequests.post(self.url_create_user, data=register_data)
        self.user_id = self.get_json_value(response_user, "id")
        self.email = register_data["email"]
        self.password = register_data["password"]

        login_data = {
            "email": self.email,
            "password": self.password
        }
        response_for_auth = MyRequests.post(self.url_login, data=login_data)
        self.auth_sid = self.get_cookie(response_for_auth, "auth_sid")
        self.csrf_token = self.get_header(response_for_auth, "x-csrf-token")

        response_for_deletion = MyRequests.delete(url=self.url_user_by_id_pattern + str(self.user_id),
                                                  headers={"x-csrf-token": self.csrf_token},
                                                  cookies={"auth_sid": self.auth_sid}
                                                  )
        Assertions.assert_status_code_is(response_for_deletion, 200)

        response = MyRequests.get(url=self.url_user_by_id_pattern + str(self.user_id),
                                  headers={"x-csrf-token": self.csrf_token},
                                  cookies={"auth_sid": self.auth_sid})

        Assertions.assert_status_code_is(response, 404)
        assert response.content.decode("utf-8") == "User not found"

    def test_delete_user_from_another_auth(self):
        register_data_1 = self.prepare_registration_data()
        response_user1 = MyRequests.post(self.url_create_user, data=register_data_1)
        self.first_user_id = self.get_json_value(response_user1, "id")

        register_data_2 = self.prepare_registration_data()
        register_data_2['firstName'] = "SecUser"
        response_user2 = MyRequests.post(self.url_create_user, data=register_data_2)
        self.email_2 = register_data_2["email"]
        self.password_2 = register_data_2["password"]

        login_data_2 = {
            "email": self.email_2,
            "password": self.password_2
        }
        response_for_auth_2 = MyRequests.post(self.url_login, data=login_data_2)
        self.auth_sid_2 = self.get_cookie(response_for_auth_2, "auth_sid")
        self.csrf_token_2 = self.get_header(response_for_auth_2, "x-csrf-token")

        response_for_deletion = MyRequests.delete(url=self.url_user_by_id_pattern + str(self.first_user_id),
                                                  headers={"x-csrf-token": self.csrf_token_2},
                                                  cookies={"auth_sid": self.auth_sid_2}
                                                  )
        Assertions.assert_status_code_is(response_for_deletion, 400)
#        print(response_for_deletion.content)
