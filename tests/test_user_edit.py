from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def setup_method(self):
        # First User Creation
        register_data_1 = self.prepare_registration_data()
        register_data_1['firstName'] = "FirstUser"
        response_user1 = MyRequests.post(self.url_create_user, data=register_data_1)
        self.user1_id = self.get_json_value(response_user1, "id")
        self.email_1 = register_data_1["email"]
        self.first_name_1 = register_data_1["firstName"]
        self.password_1 = register_data_1["password"]

        login_data_1 = {
            "email": self.email_1,
            "password": self.password_1
        }
        response_for_auth_1 = MyRequests.post(self.url_login, data=login_data_1)
        self.auth_sid_1 = self.get_cookie(response_for_auth_1, "auth_sid")
        self.csrf_token_1 = self.get_header(response_for_auth_1, "x-csrf-token")

        # Second User Creation
        register_data_2 = self.prepare_registration_data()
        register_data_2['firstName'] = "SecUser"
        response_user2 = MyRequests.post(self.url_create_user, data=register_data_2)
        self.user2_id = self.get_json_value(response_user2, "id")
        self.email_2 = register_data_2["email"]
        self.first_name_2 = register_data_2["firstName"]
        self.password_2 = register_data_2["password"]

        login_data_2 = {
            "email": self.email_2,
            "password": self.password_2
        }
        response_for_auth_2 = MyRequests.post(self.url_login, data=login_data_2)
        self.auth_sid_2 = self.get_cookie(response_for_auth_2, "auth_sid")
        self.csrf_token_2 = self.get_header(response_for_auth_2, "x-csrf-token")

    def teardown_method(self):
        # First User Deletion
        delete_user_url_1 = f'{self.url_user_by_id_pattern}{self.user1_id}'
        MyRequests.delete(delete_user_url_1,
                          headers={"x-csrf-token": self.csrf_token_1},
                          cookies={"auth_sid": self.auth_sid_1}
                          )

        # Second User Deletion
        delete_user_url_2 = f'{self.url_user_by_id_pattern}{self.user2_id}'
        MyRequests.delete(delete_user_url_2,
                          headers={"x-csrf-token": self.csrf_token_2},
                          cookies={"auth_sid": self.auth_sid_2}
                          )

    def test_edit_user_just_created(self):
        new_name = f"Name Changed from {self.first_name_1}"
        response = MyRequests.put(self.url_user_by_id_pattern + str(self.user1_id),
                                  headers={"x-csrf-token": self.csrf_token_1},
                                  cookies={"auth_sid": self.auth_sid_1},
                                  data={"firstName": new_name})

        Assertions.assert_status_code_is(response, 200)

        # GET NEW DATA
        response_user_changed = MyRequests.get(self.url_user_by_id_pattern + str(self.user1_id),
                                               headers={"x-csrf-token": self.csrf_token_1},
                                               cookies={"auth_sid": self.auth_sid_1})

        Assertions.assert_json_value_by_name(response_user_changed,
                                             "firstName",
                                             new_name,
                                             "Wrong name of user after edit")

    def test_edit_user_unauthorized(self):
        new_name = f"Name Changed from {self.first_name_1}"
        response = MyRequests.put(self.url_user_by_id_pattern + str(self.user1_id),
                                  data={"firstName": new_name})

        Assertions.assert_status_code_is(response, 400)
        assert response.content.decode("utf-8") == "Auth token not supplied"

    def test_edit_user_wrong_user_auth(self):
        new_name = f"Name Changed from {self.first_name_2}"
        response = MyRequests.put(self.url_user_by_id_pattern + str(self.user2_id),
                                  headers={"x-csrf-token": self.csrf_token_1},
                                  cookies={"auth_sid": self.auth_sid_1},
                                  data={"firstName": new_name})

        Assertions.assert_status_code_is(response, 400)
        print(response.content)

    def test_edit_user_wrong_email(self):
        new_email = f"changed.ru"
        response = MyRequests.put(self.url_user_by_id_pattern + str(self.user2_id),
                                  headers={"x-csrf-token": self.csrf_token_1},
                                  cookies={"auth_sid": self.auth_sid_1},
                                  data={"email": new_email})

        Assertions.assert_status_code_is(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format"

    def test_edit_user_name_too_short(self):
        new_name = f"N"
        response = MyRequests.put(self.url_user_by_id_pattern + str(self.user2_id),
                                  headers={"x-csrf-token": self.csrf_token_2},
                                  cookies={"auth_sid": self.auth_sid_2},
                                  data={"firstName": new_name})

        Assertions.assert_status_code_is(response, 400)
        assert response.content.decode("utf-8") == "Too short value for field firstName"
