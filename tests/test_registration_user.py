import pytest

from base_page.base_user_methods import UserAPI
from base_page.assertions import Assertions


class TestCreateUser:

    def test_create_user_success(self):
        """Успешное создание нового пользователя"""

        user_data = UserAPI.prepare_registration_data()
        response = UserAPI.create_user(user_data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        """Попытка создания нового пользователя с уже существующим email"""

        user_data = UserAPI.prepare_registration_data(email='testexample@gmail.com')
        response = UserAPI.create_user(user_data)

        Assertions.assert_status_code(response, 400)
        assert response.text == f"Users with email '{user_data['email']}' already exists", \
            f"Expected error message: 'Users with email {user_data['email']} already exists', but got: '{response.text}'"

    def test_create_user_with_invalid_email(self):
        """Попытка создания пользователя в некорректным email"""

        user_data = UserAPI.prepare_registration_data(email='testexample.com')
        response = UserAPI.create_user(user_data)

        Assertions.assert_status_code(response, 400)
        assert response.text == 'Invalid email format', \
            f'Expected error message: "Invalid email format", but got: "{response.text}"'

    @pytest.mark.parametrize('field, value, error_message', [
        ('username', '', "The value of 'username' field is too short"),
        ('firstName', '', "The value of 'firstName' field is too short"),
        ('lastName', '', "The value of 'lastName' field is too short"),
        ('password', '', "The value of 'password' field is too short"),
        ('username', 'a', "The value of 'username' field is too short"),
        ('firstName', 'a', "The value of 'firstName' field is too short"),
        ('lastName', 'a', "The value of 'lastName' field is too short"),
        ('password', 'a', "The value of 'password' field is too short"),
        ('username', 'qwerty'*50, "The value of 'username' field is too long"),
        ('firstName', 'qwerty'*50, "The value of 'firstName' field is too long"),
        ('lastName', 'qwerty'*50, "The value of 'lastName' field is too long"),
        ('password', 'qwerty'*50, "The value of 'password' field is too long")
    ])
    def test_create_user_with_empty_short_or_long_field(self, field, value, error_message):
        """Попытка создания пользователя с некорректными данными"""

        user_data = UserAPI.prepare_registration_data()
        user_data[field] = value

        response = UserAPI.create_user(user_data)

        Assertions.assert_status_code(response, 400)
        assert response.text == error_message, \
            f'Expected error message: "{error_message}", but got: "{response.text}"'
