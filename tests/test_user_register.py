from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):
    existing_email = "vinkotov@example.com"

    def test_create_new_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post(url=self.url_create_user, data=data)

        Assertions.assert_status_code_is(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_already_existing_email(self):
        data = self.prepare_registration_data(self.existing_email)

        response = MyRequests.post(url=self.url_create_user, data=data)

        Assertions.assert_status_code_is(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{self.existing_email}' already exists", \
            f"Unexpected response content {response.content}"
