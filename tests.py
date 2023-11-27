import requests
from faker import Faker
import pytest
import allure
fake = Faker()

class TestCreateUser:
    @allure.title('Проверка создания пользователя')
    def test_check_create(self, login_user):
        url = "https://stellarburgers.nomoreparties.site/api/auth/register"
        data = login_user
        response = requests.post(url, json=data)
        assert response.status_code == 200

    @allure.title('Проверка повторного создания пользователя')
    def test_check_not_create_twice(self):
        url = "https://stellarburgers.nomoreparties.site/api/auth/register"
        data = {
            "email": "annlevina1111@mail.ru",
            "password": "123456",
            "name": "имя"
        }
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
        url = "https://stellarburgers.nomoreparties.site/api/auth/register"
        response = requests.post(url, json=data)
        assert response.json()[
                   'message'] == 'Email, password and name are required fields' and response.status_code == 403

class TestLoginUser:

    @allure.title('Проверка успешной авторизации пользователя')
    def test_check_login(self):
        url = "https://stellarburgers.nomoreparties.site/api/auth/login"
        data = {
            "email": 'annlevina1111@mail.ru',
            "password": 'password123'
        }
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
        url = "https://stellarburgers.nomoreparties.site/api/auth/login"
        response = requests.post(url, json=data)
        assert response.status_code == 401 and response.json()['message'] == 'email or password are incorrect'

class TestPutUser:
    @allure.title('Проверка успешого изменения данных пользователя')
    def test_update_user_info(self):
        login_data = {
            "email": 'annlevina1112@mail.ru',
            "password": 'password123'
        }
        response = requests.post("https://stellarburgers.nomoreparties.site/api/auth/login", json=login_data)
        token = response.json()["accessToken"]
        headers = {"authorization": token}
        response2 = requests.get("https://stellarburgers.nomoreparties.site/api/auth/user", headers=headers)
        new_info = {
            "email": "annlevina1113@mail.ru",
            "name": fake.name()
        }
        response3 = requests.patch("https://stellarburgers.nomoreparties.site/api/auth/user", headers=headers,
                                  json=new_info)
        assert response3.status_code == 200
        assert response3.json()["success"] == True
        assert "user" in response3.json()
        assert "email" in response3.json()["user"]
        assert response3.json()["user"]["email"] == new_info["email"]
        assert "name" in response3.json()["user"]
        assert response3.json()["user"]["name"] == new_info["name"]
        new_info = {
            "email": "annlevina1112@mail.ru",
            "name": fake.name()
        }
        requests.patch("https://stellarburgers.nomoreparties.site/api/auth/user", headers=headers,
                                   json=new_info)

    @allure.title('Проверка успешого изменения пароля пользователя')
    def test_update_user_password(self):
        login_data = {
            "email": 'annlevina1112@mail.ru',
            "password": 'password123'
        }
        response = requests.post("https://stellarburgers.nomoreparties.site/api/auth/login", json=login_data)
        token = response.json()["accessToken"]
        headers = {"authorization": token}
        response2 = requests.get("https://stellarburgers.nomoreparties.site/api/auth/user", headers=headers)
        new_info = {
            "password": 'password'
        }
        response3 = requests.patch("https://stellarburgers.nomoreparties.site/api/auth/user", headers=headers,
                                    json=new_info)
        assert response3.status_code == 200 and response3.json()["success"] == True
        new_info = {
            "password": 'password123'
        }
        requests.patch("https://stellarburgers.nomoreparties.site/api/auth/user", headers=headers,
                        json=new_info)

    @allure.title('Проверка ошибки изменения данных неавторизованного пользователя пользователя')
    def test_not_update_user_info(self):
        new_info = {
            "email": "annlevina1113@mail.ru",
            "name": fake.name()
        }
        response = requests.patch("https://stellarburgers.nomoreparties.site/api/auth/user",
                                  json=new_info)
        assert response.status_code == 401 and response.json()['message'] == 'You should be authorised'

class TestCreateOrder:
    @allure.title('Проверка успешого создания заказа для авторизованного пользователя с ингредиентами')
    def test_create_order_authorized_user_with_ingredients(self):
        login_data = {
            "email": 'annlevina1111@mail.ru',
            "password": 'password123'
        }
        response = requests.post("https://stellarburgers.nomoreparties.site/api/auth/login", json=login_data)
        token = response.json()["accessToken"]
        headers = {"authorization": token}
        body = {"ingredients": ["61c0c5a71d1f82001bdaaa6d"]}
        response2 = requests.post("https://stellarburgers.nomoreparties.site/api/orders", json=body, headers=headers)
        assert response2.status_code == 200 and response2.json()["success"] == True

    @allure.title('Проверка создания заказа для неавторизованного пользователя с ингредиентами')
    def test_create_order_not_authorized_user_with_ingredients(self):
        body = {"ingredients": ["61c0c5a71d1f82001bdaaa6d"]}
        response = requests.post("https://stellarburgers.nomoreparties.site/api/orders", json=body)
        assert response.status_code == 200

    @allure.title('Проверка создания заказа для авторизованного пользователя без ингредиентов')
    def test_create_order_authorized_user_without_ingredients(self):
        login_data = {
            "email": 'annlevina1111@mail.ru',
            "password": 'password123'
        }
        response = requests.post("https://stellarburgers.nomoreparties.site/api/auth/login", json=login_data)
        token = response.json()["accessToken"]
        headers = {"authorization": token}
        body = {"ingredients": []}
        response2 = requests.post("https://stellarburgers.nomoreparties.site/api/orders", json=body, headers=headers)
        assert response2.status_code == 400 and response2.json()["message"] == 'Ingredient ids must be provided'

    @allure.title('Проверка создания заказа для неавторизованного пользователя без ингредиентов')
    def test_create_order_not_authorized_user_without_ingredients(self):
        body = {"ingredients": []}
        response = requests.post("https://stellarburgers.nomoreparties.site/api/orders", json=body)
        assert response.status_code == 400 and response.json()["message"] == 'Ingredient ids must be provided'

    @allure.title('Проверка создания заказа для авторизованного пользователя с невалидным хешем')
    def test_create_order_authorized_user_without_correct_ingredients(self):
        login_data = {
            "email": 'annlevina1111@mail.ru',
            "password": 'password123'
        }
        response = requests.post("https://stellarburgers.nomoreparties.site/api/auth/login", json=login_data)
        token = response.json()["accessToken"]
        headers = {"authorization": token}
        body = {"ingredients": ["61c0c5a71d1f82001bdaaa6d32432432432"]}
        response2 = requests.post("https://stellarburgers.nomoreparties.site/api/orders", json=body, headers=headers)
        assert response2.status_code == 500

class TestListOrders:
    @allure.title('Проверка запроса списка заказов для неавторизованного пользователя')
    def test_get_orders_not_authorized_user(self):
        url = "https://stellarburgers.nomoreparties.site/api/orders"
        response = requests.get(url)
        assert response.status_code == 401

    @allure.title('Проверка запроса списка заказов для авторизованного пользователя')
    def test_get_orders_authorized_user(self):
        login_data = {
            "email": 'annlevina1111@mail.ru',
            "password": 'password123'
        }
        response = requests.post("https://stellarburgers.nomoreparties.site/api/auth/login", json=login_data)
        token = response.json()["accessToken"]
        headers = {"authorization": token}
        url = "https://stellarburgers.nomoreparties.site/api/orders"
        response = requests.get(url, headers=headers)
        assert response.status_code == 200 and isinstance(response.json()["orders"], list)



