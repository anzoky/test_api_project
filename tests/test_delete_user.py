import pytest

from base_page.base_user_methods import UserAPI
from base_page.assertions import Assertions
from base_page.base_case import BaseCase


class TestDeleteUser:

    def test_delete_user_success_and_check_deleted(self):
        """Удаление только что созданного пользователя"""

        # POST-запрос на создание нового пользователя
        user_data = UserAPI.prepare_registration_data()
        response_create = UserAPI.create_user(user_data)

        # Проверка, что новый пользователь был успешно создан
        Assertions.assert_status_code(response_create, 200)
        Assertions.assert_json_has_key(response_create, 'id')
        user_id = BaseCase.get_json_value(response_create, 'id')

        # POST-запрос на авторизацию пользователя
        response_auth = UserAPI.authenticate_user(user_data['email'], user_data['password'])

        # DELETE-запрос на удаление пользователя
        response_delete = UserAPI.delete_user(user_id,
                                              headers=response_auth['token'],
                                              cookies=response_auth['cookies']
                                              )

        Assertions.assert_status_code(response_delete, 200)

        # GET-запрос на получение данных о пользователе
        response_get = UserAPI.get_user_info(user_id,
                                             headers=response_auth['token'],
                                             cookies=response_auth['cookies']
                                             )

        Assertions.assert_status_code(response_get, 404)

        error_message = 'User not found'
        assert response_get.text == error_message, \
            f'Expected error message: "{error_message}", but got: "{response_get.text}"'

    def test_delete_other_user(self):
        """Попытка удаления другого пользователя после успешной авторизации"""

        # POST-запрос на авторизацию пользователя
        response_auth = UserAPI.authenticate_user()

        # DELETE-запрос на удаление другого пользователя,
        # (в данном случае пользователь с таким ID существует)
        response_delete = UserAPI.delete_user('119303',
                                              headers=response_auth['token'],
                                              cookies=response_auth['cookies']
                                              )

        # Проверка, что сервер вернул ошибку
        Assertions.assert_status_code(response_delete, 400)
        Assertions.assert_json_has_key(response_delete, 'error')

        actual_error_message = BaseCase.get_json_value(response_delete, 'error')
        expected_error_message = 'This user can only delete their own account.'

        assert expected_error_message == actual_error_message, \
            f'Expected error message: "{expected_error_message}", but got: "{actual_error_message}"'

    def test_delete_non_existent_user(self):
        """Попытка удаления несуществующего пользователя"""

        # POST-запрос на авторизацию пользователя
        response_auth = UserAPI.authenticate_user()

        # DELETE-запрос на удаление другого пользователя,
        # (в данном случае ID некорректный)
        response_delete = UserAPI.delete_user('1a',
                                              headers=response_auth['token'],
                                              cookies=response_auth['cookies']
                                              )

        Assertions.assert_status_code(response_delete, 404)

    def test_delete_user_without_auth(self):
        """Попытка удаления пользователя без авторизации"""

        # DELETE-запрос на удаление другого пользователя,
        # (в данном случае пользователь с таким ID существует)
        response_delete = UserAPI.delete_user('119303')

        # Проверка, что сервер вернул ошибку
        Assertions.assert_status_code(response_delete, 400)
        Assertions.assert_json_has_key(response_delete, 'error')

        actual_error_message = BaseCase.get_json_value(response_delete, 'error')
        expected_error_message = 'Auth token not supplied'

        assert expected_error_message == actual_error_message, \
            f'Expected error message: "{expected_error_message}", but got: "{actual_error_message}"'
