import requests
import allure


class MyRequests:
    """
    Класс для работы с HTTP-запросами
    """
    @staticmethod
    def post(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f'POST request to URL "{url}"'):
            return MyRequests._send(url, data, headers, cookies, 'POST')

    @staticmethod
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f'GET request to URL "{url}"'):
            return MyRequests._send(url, data, headers, cookies, 'GET')

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f'PUT request to URL "{url}"'):
            return MyRequests._send(url, data, headers, cookies, 'PUT')

    @staticmethod
    def delete(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f'DELETE request to URL "{url}"'):
            return MyRequests._send(url, data, headers, cookies, 'DELETE')

    @staticmethod
    # Общий метод для отправки запросов
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str):

        url = f'https://playground.learnqa.ru/api/{url}'

        if headers is None:
            headers = {}

        if cookies is None:
            cookies = {}

        if method == 'GET':
            response = requests.get(url, params=data, headers=headers, cookies=cookies)

        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers, cookies=cookies)

        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers, cookies=cookies)

        elif method == 'DELETE':
            response = requests.delete(url, data=data, headers=headers, cookies=cookies)

        else:
            raise Exception(f'Bad HTTP method "{method}" was received')

        return response
