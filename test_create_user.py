import requests
from faker import Faker
import pytest
import allure
fake = Faker()
import dataset

class TestCreateUser:
    @allure.title('Проверка создания пользователя')
    def test_check_create(self, login_user):
        url = dataset.Data.register_url
        data = login_user
        response = requests.post(url, json=data)
        assert response.status_code == 200

    @allure.title('Проверка повторного создания пользователя')
    def test_check_not_create_twice(self):
        url = dataset.Data.register_url
        data = dataset.Data.create_user_twice_data
        response = requests.post(url, json=data)
        assert response.json()[
                   'message'] == 'User already exists' and response.status_code == 403

    @allure.title('Проверка создания пользователя без ввода данных')
    @allure.title('Проверка создания пользователя без емейла')
    @allure.title('Проверка создания пользователя без пароля')
    @allure.title('Проверка создания пользователя без имени')
    @pytest.mark.parametrize("data", [
        {
        },
        {
            "password": fake.password(),
            "name": fake.name()
        },
        {
            "email": fake.email(),
            "name": fake.name()
        },
        {
            "email": fake.email(),
            "password": fake.password()
        }
    ])
    def test_check_no_field(self, data):
        url = dataset.Data.register_url
        response = requests.post(url, json=data)
        assert response.json()[
                   'message'] == 'Email, password and name are required fields' and response.status_code == 403