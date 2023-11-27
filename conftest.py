import requests
from faker import Faker
import pytest
fake = Faker()

@pytest.fixture
def login_user():
    data = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }
    yield data
    login_url = "https://stellarburgers.nomoreparties.site/api/auth/login"
    login_data = {
        "email": data['email'],
        "password": data['password']
    }
    delete_url = f"https://stellarburgers.nomoreparties.site/api/auth/user"
    requests.delete(delete_url)