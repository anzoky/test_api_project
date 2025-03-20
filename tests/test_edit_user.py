import pytest
import allure

from base_page.base_user_methods import UserAPI
from base_page.assertions import Assertions
from base_page.base_case import BaseCase


@allure.epic('Изменение данных о пользователе')
class TestUserEdit:

    @allure.story('Успешное изменение имени пользователя')
    def test_edit_user_success(self):
        """Проверка редактирования пользователя
        В данном случае меняем имя нового пользователя после его создания"""

        # POST-запрос на создание нового пользователя
        user_data = UserAPI.prepare_registration_data()
        response_create = UserAPI.create_user(user_data)

        # Проверка, что новый пользователь был успешно создан
        Assertions.assert_status_code(response_create, 200)
        Assertions.assert_json_has_key(response_create, 'id')
        user_id = BaseCase.get_json_value(response_create, 'id')

        # POST-запрос на авторизацию пользователя
        response_auth = UserAPI.authenticate_user(user_data['email'], user_data['password'])

        # PUT-запрос на редактирование пользователя
        name_for_change = 'Someone new'
        response_update = UserAPI.update_user(user_id,
                                              user_data={'firstName': name_for_change},
                                              headers=response_auth['token'],
                                              cookies=response_auth['cookies']
                                              )

        # Проверка, что редактирование прошло успешно
        Assertions.assert_status_code(response_update, 200)

        # GET-запрос на получение данных о пользователе
        response_get = UserAPI.get_user_info(user_id,
                                             headers=response_auth['token'],
                                             cookies=response_auth['cookies']
                                             )

        # Проверка, что изменение имени прошло успешно
        changed_name = BaseCase.get_json_value(response_get, 'firstName')
        Assertions.assert_status_code(response_get, 200)
        assert name_for_change == changed_name, \
            f'The name has not been changed. Expected: "{name_for_change}", actual: "{changed_name}"'

    @allure.story('Изменение данных у неавторизованного пользователя')
    def test_edit_user_unauthorized(self):
        """Попытка редактирования пользователя без авторизации"""

        # POST-запрос на создание нового пользователя
        user_data = UserAPI.prepare_registration_data()
        response_create = UserAPI.create_user(user_data)

        # Проверка, что новый пользователь был успешно создан
        Assertions.assert_status_code(response_create, 200)
        Assertions.assert_json_has_key(response_create, 'id')
        user_id = BaseCase.get_json_value(response_create, 'id')

        # PUT-запрос на редактирование пользователя без авторизации
        name_for_change = 'Someone new'
        response_update = UserAPI.update_user(user_id,
                                              user_data={'firstName': name_for_change}
                                              )

        # Проверка, что сервер вернул ошибку из-за отсутствия авторизации
        Assertions.assert_status_code(response_update, 400)
        Assertions.assert_json_has_key(response_update, 'error')

        actual_error_message = BaseCase.get_json_value(response_update, 'error')
        expected_error_message = 'Auth token not supplied'

        assert expected_error_message == actual_error_message, \
            f'Expected error message: "{expected_error_message}", but got: "{actual_error_message}"'

    @allure.story('Изменение email пользователя на некорректный')
    def test_edit_user_invalid_email(self):
        """Попытка редактирования email пользователя на некорректный"""

        # POST-запрос на создание нового пользователя
        user_data = UserAPI.prepare_registration_data()
        response_create = UserAPI.create_user(user_data)

        # Проверка, что новый пользователь был успешно создан
        Assertions.assert_status_code(response_create, 200)
        Assertions.assert_json_has_key(response_create, 'id')
        user_id = BaseCase.get_json_value(response_create, 'id')

        # POST-запрос на авторизацию пользователя
        response_auth = UserAPI.authenticate_user(user_data['email'], user_data['password'])

        # PUT-запрос на редактирование email пользователя
        email_for_change = 'invalid_email.com'
        response_update = UserAPI.update_user(user_id,
                                              user_data={'email': email_for_change},
                                              headers=response_auth['token'],
                                              cookies=response_auth['cookies']
                                              )
        # Проверка, что сервер вернул ошибку из-за неверного формата email
        Assertions.assert_status_code(response_update, 400)
        Assertions.assert_json_has_key(response_update, 'error')

        actual_error_message = BaseCase.get_json_value(response_update, 'error')
        expected_error_message = 'Invalid email format'

        assert expected_error_message == actual_error_message, \
            f'Expected error message: "{expected_error_message}", but got: "{actual_error_message}"'

    @pytest.mark.parametrize('name, expected_error', [
        ('', 'The value for field `firstName` is too short'),
        ('a', 'The value for field `firstName` is too short'),
        ('qwerty'*100, 'The value for field `firstName` is too long')
    ])
    @allure.story('Изменение имени пользователя на некорректное')
    def test_edit_user_incorrect_firstname(self, name, expected_error):
        """Попытка редактирования имени пользователя на пустое, короткое или слишком длинное"""

        # POST-запрос на создание нового пользователя
        user_data = UserAPI.prepare_registration_data()
        response_create = UserAPI.create_user(user_data)

        # Проверка, что новый пользователь был успешно создан
        Assertions.assert_status_code(response_create, 200)
        Assertions.assert_json_has_key(response_create, 'id')
        user_id = BaseCase.get_json_value(response_create, 'id')

        # POST-запрос на авторизацию пользователя
        response_auth = UserAPI.authenticate_user(user_data['email'], user_data['password'])

        # PUT-запрос на редактирование пользователя
        name_for_change = name
        response_update = UserAPI.update_user(user_id,
                                              user_data={'firstName': name_for_change},
                                              headers=response_auth['token'],
                                              cookies=response_auth['cookies']
                                              )

        # Проверка, что сервер вернул ошибку из-за некорректного имени
        Assertions.assert_status_code(response_update, 400)
        Assertions.assert_json_has_key(response_update, 'error')

        actual_error_message = BaseCase.get_json_value(response_update, 'error')
        assert actual_error_message == expected_error,  \
            f'Expected error message: "{expected_error}", but got: "{actual_error_message}"'
