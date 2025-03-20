## Описание
API-тесты на регистрацию, аутентицикаю, изенение, удаление пользователя и получение данных о пользователе

## Технологии
- **Pytest** – тестовый фреймворк
- **Requests** - HTTP-запросы
- **Allure** – генерация отчётов


- ## Как запустить проект?
1. **Установите зависимости:**  
   ```bash
   pip install -r requirements.txt

2. **Запустите тесты:**
    ```bash
    pytest --alluredir=allure-results

3. **Сгенерируйте и откройте Allure-отчёт:**
    ```bash
   allure serve allure-results
    
**Аллюр отчет**
![Allure Report](https://github.com/anzoky/test_api_project/blob/main/allure_report_api.png)
