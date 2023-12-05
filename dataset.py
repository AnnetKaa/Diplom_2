class Data:
    login_url = "https://stellarburgers.nomoreparties.site/api/auth/login"
    put_url = f"https://stellarburgers.nomoreparties.site/api/auth/user"
    register_url = "https://stellarburgers.nomoreparties.site/api/auth/register"
    orders_url = "https://stellarburgers.nomoreparties.site/api/orders"

    login_data = {
        "email": 'annlevina1111@mail.ru',
        "password": 'password123'
    }

    create_user_twice_data = {
        "email": "annlevina1111@mail.ru",
        "password": "123456",
        "name": "имя"
    }

    update_user_data = {
            "email": 'annlevina1112@mail.ru',
            "password": 'password123'
        }
