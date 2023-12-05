import requests
from faker import Faker
import pytest
import allure
fake = Faker()
import dataset

class TestLoginUser:

    @allure.title('Проверка успешной авторизации пользователя')
    def test_check_login(self):
        url = dataset.Data.login_url
        data = dataset.Data.login_data
        response = requests.post(url, json=data)
        assert response.status_code == 200


    @allure.title('Проверка авторизации пользователя с некорректным паролем')
    @allure.title('Проверка авторизации пользователя с некорректным логином')
    @allure.title('Проверка авторизации пользователя без логина')
    @allure.title('Проверка авторизации пользователя с несуществующим логином')
    @pytest.mark.parametrize("data", [
        {
            "email": 'annlevina1111@mail.ru',
            "password": 'password'
        },
        {
            "email": '1111annlevina1111@mail.ru',
            "password": 'password123'
        },
        {
            "password": 'password123'
        },
        {
            "email": "abracadabra",
            "password": "password123"
        }
    ])
    def test_check_incorrect_password(self, data):
        url = dataset.Data.login_url
        response = requests.post(url, json=data)
        assert response.status_code == 401 and response.json()['message'] == 'email or password are incorrect'