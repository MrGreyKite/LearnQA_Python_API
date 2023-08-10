from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, property_name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response isn't in JSON format. Response is: '{response.text}'"

        assert property_name in response_as_dict, f"Response doesn't have a property '{property_name}'"
        assert response_as_dict[property_name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, key_name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response isn't in JSON format. Response is: '{response.text}'"

        assert key_name in response_as_dict, f"Response doesn't have a property '{key_name}'"

    @staticmethod
    def assert_status_code_is(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, f"Unexpected status code - {response.status_code}, " \
                                                             f"expected status code was - {expected_status_code}"
