import requests
from faker import Faker
import pytest
import allure
fake = Faker()
import dataset

class TestCreateOrder:
    @allure.title('Проверка успешого создания заказа для авторизованного пользователя с ингредиентами')
    def test_create_order_authorized_user_with_ingredients(self):
        response = requests.post(dataset.Data.login_url, json=dataset.Data.login_data)
        token = response.json()["accessToken"]
        headers = {"authorization": token}
        body = {"ingredients": ["61c0c5a71d1f82001bdaaa6d"]}
        response2 = requests.post(dataset.Data.orders_url, json=body, headers=headers)
        assert response2.status_code == 200 and response2.json()["success"] == True

    @allure.title('Проверка создания заказа для неавторизованного пользователя с ингредиентами')
    def test_create_order_not_authorized_user_with_ingredients(self):
        body = {"ingredients": ["61c0c5a71d1f82001bdaaa6d"]}
        response = requests.post(dataset.Data.orders_url, json=body)
        assert response.status_code == 200

    @allure.title('Проверка создания заказа для авторизованного пользователя без ингредиентов')
    def test_create_order_authorized_user_without_ingredients(self):
        login_data = dataset.Data.login_data
        response = requests.post(dataset.Data.login_url, json=login_data)
        token = response.json()["accessToken"]
        headers = {"authorization": token}
        body = {"ingredients": []}
        response2 = requests.post(dataset.Data.orders_url, json=body, headers=headers)
        assert response2.status_code == 400 and response2.json()["message"] == 'Ingredient ids must be provided'

    @allure.title('Проверка создания заказа для неавторизованного пользователя без ингредиентов')
    def test_create_order_not_authorized_user_without_ingredients(self):
        body = {"ingredients": []}
        response = requests.post(dataset.Data.orders_url, json=body)
        assert response.status_code == 400 and response.json()["message"] == 'Ingredient ids must be provided'

    @allure.title('Проверка создания заказа для авторизованного пользователя с невалидным хешем')
    def test_create_order_authorized_user_without_correct_ingredients(self):
        login_data = dataset.Data.login_data
        response = requests.post(dataset.Data.login_url, json=login_data)
        token = response.json()["accessToken"]
        headers = {"authorization": token}
        body = {"ingredients": ["61c0c5a71d1f82001bdaaa6d32432432432"]}
        response2 = requests.post(dataset.Data.orders_url, json=body, headers=headers)
        assert response2.status_code == 500