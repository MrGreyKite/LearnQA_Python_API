from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_user_just_created(self):
        # CREATE NEW USER
        register_data = self.prepare_registration_data()
        response_for_register = MyRequests.post(self.url_create_user, data=register_data)

        Assertions.assert_status_code_is(response_for_register, 200)
        Assertions.assert_json_has_key(response_for_register, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response_for_register, "id")

        # LOG IN
        login_data = {
            "email": email,
            "password": password
        }
        response_for_auth = MyRequests.post(self.url_login, data=login_data)
        auth_sid = self.get_cookie(response_for_auth, "auth_sid")
        csrf_token = self.get_header(response_for_auth, "x-csrf-token")

        # EDIT
        new_name = f"Name Changed from {first_name}"
        response = MyRequests.put(self.url_user_by_id_pattern + str(user_id),
                                  headers={"x-csrf-token": csrf_token},
                                  cookies={"auth_sid": auth_sid},
                                  data={"firstName": new_name})

        Assertions.assert_status_code_is(response, 200)

        # GET NEW DATA
        response_user_changed = MyRequests.get(self.url_user_by_id_pattern + str(user_id),
                                               headers={"x-csrf-token": csrf_token},
                                               cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response_user_changed,
                                             "firstName",
                                             new_name,
                                             "Wrong name of user after edit")
