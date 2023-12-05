import requests
from faker import Faker
import pytest
import allure
fake = Faker()
import dataset

class TestPutUser:
    @allure.title('Проверка успешого изменения данных пользователя')
    def test_update_user_info(self):
        login_data = dataset.Data.update_user_data
        response = requests.post(dataset.Data.login_url, json=login_data)
        token = response.json()["accessToken"]
        headers = {"authorization": token}
        response2 = requests.get(dataset.Data.put_url, headers=headers)
        new_info = {
            "email": "annlevina1113@mail.ru",
            "name": fake.name()
        }
        response3 = requests.patch(dataset.Data.put_url, headers=headers,
                                  json=new_info)
        assert response3.status_code == 200 and response3.json()["success"] == True
        new_info = {
            "email": "annlevina1112@mail.ru",
            "name": fake.name()
        }
        requests.patch(dataset.Data.put_url, headers=headers,
                                   json=new_info)

    @allure.title('Проверка успешого изменения пароля пользователя')
    def test_update_user_password(self):
        login_data = dataset.Data.update_user_data
        response = requests.post(dataset.Data.login_url, json=login_data)
        token = response.json()["accessToken"]
        headers = {"authorization": token}
        response2 = requests.get(dataset.Data.put_url, headers=headers)
        new_info = {
            "password": 'password'
        }
        response3 = requests.patch(dataset.Data.put_url, headers=headers,
                                    json=new_info)
        new_info2 = {
            "password": 'password123'
        }
        requests.patch(dataset.Data.put_url, headers=headers,
                       json=new_info2)
        assert response3.status_code == 200 and response3.json()["success"] == True


    @allure.title('Проверка ошибки изменения данных неавторизованного пользователя пользователя')
    def test_not_update_user_info(self):
        new_info = {
            "email": "annlevina1113@mail.ru",
            "name": fake.name()
        }
        response = requests.patch(dataset.Data.put_url,
                                  json=new_info)
        assert response.status_code == 401 and response.json()['message'] == 'You should be authorised'