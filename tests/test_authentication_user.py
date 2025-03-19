import pytest

from base_page.base_user_methods import UserAPI
from base_page.assertions import Assertions
from base_page.base_case import BaseCase


class TestAuthenticationUser:

    def test_login_new_user(self):
        """Тест на проверку успешной аутентификации нового пользователя"""

        # Запрос на создание нового пользователя
        user_data = UserAPI.prepare_registration_data()
        response_create = UserAPI.create_user(user_data)

        Assertions.assert_status_code(response_create, 200)

        # Запрос на аутентификацию пользователя
        response_auth = UserAPI.authenticate_user(user_data['email'], user_data['password'])

        # Проверка, что сервер вернул token, cookie и user_id
        assert response_auth['user_id'] is not None, 'The response does not contain "user_id"'
        assert response_auth['token'] is not None, 'The response does not contain "token"'
        assert response_auth['cookies'] is not None, 'The response does not contain "cookie"'

    @pytest.mark.parametrize('email', ['test+example@gmail.com',
                                       ' testexample@gmail.com',
                                       'testexample@gmail.com ',
                                       'test.example@gmail.com',
                                       'test@example@gmail.com',
                                       'testexample@.com'
                                       'testexamplegmail.com',
                                       'TestExample@gmail.com',
                                       'тест@пример.рф',
                                       '测试@example.com',
                                       '😀@example.com',
                                       '" OR "1"="1',
                                       '" OR "1"="1" --',
                                       '"; DROP TABLE users; --',
                                       '<script>alert("XSS")</script>',
                                       '><script>alert("Hacked")</script>',
                                       '<img src=x onerror=alert("XSS")>'
                                       ])
    def test_auth_with_invalid_email(self, email):
        """Проверка аутентификации пользователя с неверными и некорректными email, но верным паролем,
        а также с потенциальными XSS-атакой и SQL-инъекцией"""

        user_data = {
            'email': email,
            'password': 'qwerty123'
        }

        # POST-запрос на аутентификацию пользователя
        response = UserAPI.login_user(user_data)
        print(response.text)

        error_message = 'Invalid username/password supplied'

        Assertions.assert_status_code(response, 400)
        assert response.text == error_message, \
            f'Expected error message: "{error_message}", but got: "{response.text}"'

    @pytest.mark.parametrize('password', ['Qwerty123',
                                          '!@#$%^&*',
                                          'qwerty123 ',
                                          ' qwerty123',
                                          'qwerty123'*50,
                                          '密码123',
                                          'пароль😀',
                                          'пароль123',
                                          '" OR "1"="1',
                                          '" OR "1"="1" --',
                                          '"; DROP TABLE users; --',
                                          '<script>alert("XSS")</script>',
                                          '><script>alert("Hacked")</script>',
                                          '<img src=x onerror=alert("XSS")>'
                                          ])
    def test_auth_with_invalid_password(self, password):
        """Проверка аутентификации пользователя с неверными и некорректными паролями, но верным email,
        а также с потенциальными XSS-атакой и SQL-инъекцией"""

        user_data = {
            'email': 'testexample@gmail.com',
            'password': password
        }

        # POST-запрос на аутентификацию пользователя
        response = UserAPI.login_user(user_data)

        print(response.text)
        error_message = 'Invalid username/password supplied'

        Assertions.assert_status_code(response, 400)
        assert response.text == error_message, \
            f'Expected error message: "{error_message}", but got: "{response.text}"'

    @pytest.mark.parametrize('email, password', [
        ('', 'password123'),
        ('testexample@gmail.com', ''),
        ('', '')
    ])
    def test_auth_with_empty_fields(self, email, password):
        """Проверка аутентификации пользователя с пустыми полями"""

        user_data = {
            'email': email,
            'password': password
        }

        # POST-запрос на аутентификацию пользователя
        response = UserAPI.login_user(user_data)

        error_message = 'Invalid username/password supplied'

        Assertions.assert_status_code(response, 400)
        assert response.text == error_message, \
            f'Expected error message: "{error_message}", but got: "{response.text}"'
