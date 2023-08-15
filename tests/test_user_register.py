import pytest

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

    def test_create_user_invalid_email(self):
        data = self.prepare_registration_data('invalid_mail.ru')

        response = MyRequests.post(url=self.url_create_user, data=data)
        print(response.content)
        Assertions.assert_status_code_is(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format"

    @pytest.mark.parametrize('empty_field', ['username', 'firstName', 'lastName', 'email', 'password'])
    def test_create_user_missing_field(self, empty_field):
        data = self.prepare_registration_data()

        data.pop(empty_field)
        response = MyRequests.post(url=self.url_create_user, data=data)
        Assertions.assert_status_code_is(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {empty_field}"

    def test_create_user_too_short_name(self):
        data = self.prepare_registration_data()
        data['username'] = "t"
        response = MyRequests.post(url=self.url_create_user, data=data)
        Assertions.assert_status_code_is(response, 400)
        assert response.content.decode("utf-8") == "The value of \'username\' field is too short"

    def test_create_user_too_long_name(self):
        data = self.prepare_registration_data()
        data['username'] = "test_user" * 50
        response = MyRequests.post(url=self.url_create_user, data=data)
        Assertions.assert_status_code_is(response, 400)
        assert response.content.decode("utf-8") == "The value of \'username\' field is too long"
