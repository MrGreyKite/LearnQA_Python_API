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
