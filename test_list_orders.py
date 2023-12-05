import requests
from faker import Faker
import pytest
import allure
fake = Faker()
import dataset

class TestListOrders:
    @allure.title('Проверка запроса списка заказов для неавторизованного пользователя')
    def test_get_orders_not_authorized_user(self):
        url = dataset.Data.orders_url
        response = requests.get(url)
        assert response.status_code == 401

    @allure.title('Проверка запроса списка заказов для авторизованного пользователя')
    def test_get_orders_authorized_user(self):
        login_data = dataset.Data.login_data
        response = requests.post(dataset.Data.login_url, json=login_data)
        token = response.json()["accessToken"]
        headers = {"authorization": token}
        url = dataset.Data.orders_url
        response = requests.get(url, headers=headers)
        assert response.status_code == 200 and isinstance(response.json()["orders"], list)