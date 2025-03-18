import json


class BaseCase:
    """Класс с вспомогательными методами для тестов"""

    @staticmethod
    def get_cookie(response, cookie_name):
        """Получает значение куки из ответа по имени куки"""

        assert cookie_name in response.cookies, f'There is not cookie "{cookie_name}" in the response'
        return response.cookies[cookie_name]

    @staticmethod
    def get_header(response, header_name):
        """Получает значение заголовка из ответа по его имени"""

        assert header_name in response.headers, f'There is not header "{header_name}" in the response'
        return response.headers[header_name]

    @staticmethod
    def get_json_value(response, name):
        """Получает значение из JSON-ответа по его имени"""
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecoderError:
            assert False, f'Response is not in JSON format. Response text is "{response.text}"'
        assert name in response_as_dict, f'Response JSON doesn`t have key "{name}"'
        return response_as_dict[name]

