import pytest

from base_page.base_user_methods import UserAPI
from base_page.assertions import Assertions


class TestGetUser:

    def test_get_user_without_authentication(self):
        """Получение информации о пользователе по ID без аутентификации
        Сервер должен вернуть только username пользователя"""

        # Отправка GET-запроса с ID пользователя (в данном случае, пользователь с таким ID существует)
        response = UserAPI.get_user_info('119303')

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_no_keys(response, ['email', 'firstName', 'lastName'])

    def test_get_user_with_authentication(self):
        """Получение информации о пользователе с аутентификацией
        Сервер должен вернуть username, email, firstName, lastName"""

        # Отправка POST-запроса на аутентификацию с email и password
        response1 = UserAPI.authenticate_user()

        # Оправка GET-запроса на получение данных о пользователе и использованием аутентификации
        response2 = UserAPI.get_user_info(response1['user_id'],
                                          headers=response1['token'],
                                          cookies=response1['cookies']
                                          )

        expected_fields = ['id', 'username', 'email', 'firstName', 'lastName']

        # Проверка, что сервер вернул все ожидаемые поля
        Assertions.assert_status_code(response2, 200)
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_other_user_data_with_auth(self):
        """Получение информации о другом пользователе с аутентификацией
        (в ответе должны быть скрыты все поля, кроме 'username')"""

        # Отправка POST-запроса на аутентификацию с email и password
        response1 = UserAPI.authenticate_user()

        # Отправка GET-запроса на получение информации о пользователе с использованием аутентификации,
        # (используется ID другого пользователя)
        response2 = UserAPI.get_user_info('119303',
                                          headers=response1['token'],
                                          cookies=response1['cookies'])

        Assertions.assert_status_code(response2,  200)
        Assertions.assert_json_has_key(response2, 'username')
        Assertions.assert_json_has_no_keys(response2, ['email', 'firstName', 'lastName'])

    def test_get_nonexistent_user(self):
        """Получение информации о несуществующем пользователе"""

        # Отправка GET-запроса с ID пользователя (в данном случае, пользователя с таким ID не существует)
        response = UserAPI.get_user_info('9999999')

        Assertions.assert_status_code(response, 404)
        assert response.text == 'User not found', \
            f'Expected error message: "User not found", but got: "{response.text}"'

    def test_get_user_with_invalid_auth(self):
        """Попытка получения информации о пользователе с ошибкой аутентификации
        (неверные token, cookie, но верный user_id)
        Сервер должен вернуть только username пользователя"""

        # Отправка POST-запроса на аутентификацию с email и password
        response1 = UserAPI.authenticate_user()

        # Неверные данные для аутентификации
        headers = {"x-csrf-token": "invalid_token"}
        cookies = {"auth_sid": "invalid_cookie"}

        # Отправка GET-запроса на получение информации о пользователе с использованием аутентификации
        response2 = UserAPI.get_user_info(response1['user_id'],
                                          headers=headers,
                                          cookies=cookies)

        Assertions.assert_status_code(response2,  200)
        Assertions.assert_json_has_key(response2, 'username')
        Assertions.assert_json_has_no_keys(response2, ['email', 'firstName', 'lastName'])
