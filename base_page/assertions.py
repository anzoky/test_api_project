import json


class Assertions:
    """Класс для проверки API-ответов"""

    @staticmethod
    def assert_status_code(response, expected_code):
        """Проверяет статус-код ответа"""
        assert response.status_code == expected_code, \
            f'Unexpected status_code: {response.status_code}. Expected: {expected_code}'

    @staticmethod
    def assert_json_has_key(response, key):
        """Проверяет, что ключ есть в JSON-ответе"""
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in JSON format. Response text is "{response.text}"'
        assert key in response_as_dict, f'Response JSON doesn`t have key {key}'

    @staticmethod
    def assert_json_has_keys(response, keys):
        """Проверяет, что все ключи есть в JSON"""
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in JSON format. Response text is "{response.text}"'
        for key in keys:
            assert key in response_as_dict, f'Response JSON doesn`t have keys {key}'

    @staticmethod
    def assert_json_has_no_key(response, key):
        """Проверяет, что ключа нет в JSON-ответе"""
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in JSON format. Response text is "{response.text}"'
        assert key not in response_as_dict, f'Response JSON shouldn`t have key {key}. But it is present'

    @staticmethod
    def assert_json_has_no_keys(response, keys):
        """Проверяет, что все ключи есть в JSON"""
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in JSON format. Response text is "{response.text}"'
        for key in keys:
            assert key not in response_as_dict, f'Response JSON doesn`t have keys {key}'
