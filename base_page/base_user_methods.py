from datetime import datetime

from base_page.api_requests import MyRequests
from base_page.assertions import Assertions
from base_page.base_case import BaseCase


class UserAPI:

    @staticmethod
    def authenticate_user(email: str, password: str):
        """Метод для аутентификации пользователя и получения token, cookie, ID"""

        # Данные для аутентификации пользователя
        data = {'email': email, 'password': password}

        # Запрос на аутентификацию
        response = UserAPI.login_user(data)
        Assertions.assert_status_code(response, 200)

        # Извлекаем и возвращаем cookie, token, user_id из ответа
        return {
            'headers': {'x-csrf-token': BaseCase.get_header(response, 'x-csrf-token')},
            'cookies': {'auth_sid': BaseCase.get_cookie(response, 'auth_sid')},
            'user_id': BaseCase.get_json_value(response, 'user_id')
        }

    @staticmethod
    def prepare_registration_data(email=None, **kwargs):
        """
        Подготовка данных для регистрации пользователя
        """
        if email is None:
            random = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"test{random}@example.com"
        data = {
            'password': 'qwerty123',
            'username': 'JonSmit',
            'firstName': 'Jon',
            'lastName': 'Smit',
            'email': email
        }
        # Значения обновляются в словаре данными из kwargs
        data.update(kwargs)
        return data

    @staticmethod
    def create_user(user_data, headers=None, cookies=None):
        """Создаёт пользователя"""
        return MyRequests.post(f'user', user_data, headers=headers, cookies=cookies)

    @staticmethod
    def delete_user(user_id, headers=None, cookies=None):
        """Удаляет пользователя (требуется аутентификация)"""
        return MyRequests.delete(f'user/{user_id}', headers=headers, cookies=cookies)

    @staticmethod
    def login_user(user_data):
        """Аутентификация пользователя"""
        return MyRequests.post(f'user/login', user_data)

    @staticmethod
    def get_user_info(user_id, headers=None, cookies=None):
        """Получает данные пользователя (требует авторизации)"""
        return MyRequests.get(f'user/{user_id}', headers=headers, cookies=cookies)

    @staticmethod
    def update_user(user_id, user_data, headers=None, cookies=None):
        """Обновляет данные пользователя (требуется аутентификация)"""
        return MyRequests.put(f'user/{user_id}', user_data, headers=headers, cookies=cookies)

