import requests
from faker import Faker
import pytest
fake = Faker()
import dataset

@pytest.fixture
def login_user():
    data = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }
    yield data
    login_url = dataset.Data.login_url
    login_data = {
        "email": data['email'],
        "password": data['password']
    }
    delete_url = dataset.Data.put_url
    requests.delete(delete_url)