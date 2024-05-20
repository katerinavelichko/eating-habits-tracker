from app import app, db
from .views import load_user
from .UserLogin import UserLogin
from .models import Users, QuestionsSleep, Diary

from flask import session, url_for, request
from flask_wtf import csrf
from flask_login import logout_user, login_user, current_user
import secrets

import json
from datetime import date, timedelta, datetime
import pytest
from unittest.mock import patch

LOGIN_EMAIL = 'login_email@example.com'
LOGIN_NAME = 'login_test_name'
LOGIN_PASSWORD = 'login_test_password'
LOGIN_DATE = date.today() - timedelta(days=1)


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def login(name, email, password, date_of_registration, client):
    new_user = Users(name=name, email=email, password=password, date_of_registration=date_of_registration)
    db.session.add(new_user)
    db.session.commit()
    response = client.post('/login', data={'email': email, 'password': password})


def logout(email):
    user = Users.query.filter_by(email=email).first()
    db.session.delete(user)
    db.session.commit()
    logout_user()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


def test_soon(client):
    login(LOGIN_NAME, LOGIN_EMAIL, LOGIN_PASSWORD, LOGIN_DATE, client)
    response = client.get('/soon')
    assert response.data == 'Скоро тут что-то будет'.encode('utf-8')
    logout(LOGIN_EMAIL)


# авторизация несуществующего пользователя
def test_login_nonexistent_user(client):
    response = client.post('/login', data={'email': 'nonexistent_user@example.com', 'password': 'nonexistent'})
    assert response.status_code == 200
    assert 'Неверный email или пароль'.encode('utf-8') in response.data
    assert b'<!DOCTYPE html>' in response.data


# авторизация существующего пользователя
def test_login_real_user(client):
    email = 'valid@example.com'
    password = 'validpassword'

    # добавляем пользователя в бд
    new_user = Users(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    response = client.post('/login', data={'email': email, 'password': password})

    # проверяем, что страница перенаправляет пользователя
    assert response.status_code == 302
    assert response.location == '/'

    assert Users.query.filter_by(email=email).first() is not None
    assert b'<!doctype html>' in response.data

    logout(email)


def test_tracker_form(client):
    login(LOGIN_NAME, LOGIN_EMAIL, LOGIN_PASSWORD, LOGIN_DATE, client)
    response = client.get('/diary')
    assert response.status_code == 200
    logout(LOGIN_EMAIL)


def test_surveys(client):
    login(LOGIN_NAME, LOGIN_EMAIL, LOGIN_PASSWORD, LOGIN_DATE, client)
    response = client.get('/questions')
    assert response.status_code == 200
    logout(LOGIN_EMAIL)


# регистрация с валидными данными
def test_create_user_valid_data(client):
    response = client.get('/signup')
    assert response.status_code == 200

    csrf_token = csrf.generate_csrf()
    response = client.post('/signup',
                           data={'name': 'testname', 'email': 'valid_email@example.com', 'password': '12345678',
                                 'csrf_token': csrf_token})
    assert response.status_code == 302
    assert Users.query.filter_by(email='valid_email@example.com').first() is not None

    logout('valid_email@example.com')


# регистрация с невалидными данными
@pytest.mark.parametrize("email, password", [
    ('invalid_email', 'valid_password'), ('validemail@example.com', 'invalid')
])
def test_create_user_invalid_data(client, email, password):
    response = client.get('/signup')
    assert response.status_code == 200
    csrf_token = csrf.generate_csrf()
    response = client.post('/signup',
                           data={'name': 'testname', 'email': email, 'password': password,
                                 'csrf_token': csrf_token})

    assert 'Некорректный email'.encode('utf-8') in response.data
    assert Users.query.filter_by(email=email).first() is None


# регистрация существующего пользователя
# def test_create_user_who_exists(client):
#     login(LOGIN_NAME, LOGIN_EMAIL, LOGIN_PASSWORD, client)
#     csrf_token = secrets.token_urlsafe(32)
#     session['csrf_token'] = csrf_token
#     # name = request.form.get('name')
#     # email = request.form.get('email')
#     # password = request.form.get('password')
#     # print(name, email, password)
#     response = client.post('/signup',
#                            data={'name': LOGIN_NAME, 'email': LOGIN_EMAIL, 'password': LOGIN_PASSWORD,
#                                  'csrf_token': csrf_token})
#     print(not Users.query.filter_by(email=LOGIN_EMAIL).first())
#     print(response.status_code)
#     print(response.location)
#     # assert response.status_code == 302
#     # assert response.location == url_for('unsuccess', _external=True)
#     # assert Users.query.filter_by(email=LOGIN_EMAIL).first() is not None
#     logout(LOGIN_EMAIL)


def test_receive_data(client):
    login(LOGIN_NAME, LOGIN_EMAIL, LOGIN_PASSWORD, LOGIN_DATE, client)

    data = {
        "sex": "М",
        "tofu": "Да",
        "fresh_cheeses": "Нет",
        "processed_meat": "Да",
        "play_sport": "Да",
        "eat_weekend": "Да, я ем в ресторанах",
        "sugary_drinks": 3,
        "cows_milk": "Да",
        "miss_meals": "Нет",
        "vegetable_drinks": "Иногда",
        "eat_fast": "Нет",
        "cooked_vegetables": "Да",
        "low_fat_yogurt": "Нет",
        "wake_up_eat_night": "Нечасто (около 1-го раза в месяц)",
        "alcoholic_beverages": 2,
        "eat_uncontrollably": "Никогда",
        "whole_grains_food": "Да",
        "eggs": "Иногда",
        "fruits": "Да",
        "fish": "Иногда",
        "meat": "Да",
        "nuts": "Нет",
        "hungry_during_day": "Днем"
    }

    response = client.post('/receive_data', json=data)
    assert response.status_code == 200

    questions_sleep = QuestionsSleep.query.filter_by(user_id=current_user.get_id()).first()
    assert questions_sleep is not None
    assert questions_sleep.sex == "М"
    assert questions_sleep.tofu == "Да"
    db.session.delete(questions_sleep)
    db.session.commit()
    logout(LOGIN_EMAIL)


def test_load_user():
    with patch.object(UserLogin, 'from_db') as mock_from_db:
        user_id = 1
        loaded_user = load_user(user_id)
        mock_from_db.assert_called_once_with(user_id)


@patch('app.views.logout_user')
def test_logout_redirects_to_login(mock_logout_user, client):
    mock_logout_user.return_value = None
    response = client.get('/logout')

    mock_logout_user.assert_called_once()
    assert response.status_code == 302
    assert response.location == '/login'


def test_callories_from_forms(client):
    login(LOGIN_NAME, LOGIN_EMAIL, LOGIN_PASSWORD, LOGIN_DATE, client)

    data = [{'name': 'яблоко', 'value': 100}]

    response = client.post('/receive_callories', json=data)
    assert response.status_code == 200

    diary = Diary.query.filter_by(user_id=current_user.get_id()).first()
    assert diary is not None
    assert diary.product_name == "яблоко"
    assert diary.grams == 100
    db.session.delete(diary)
    db.session.commit()
    logout(LOGIN_EMAIL)


def test_unsuccess(client):
    response = client.get('/signup/unsuccess')
    assert response.status_code == 200


def test_profile(client):
    login(LOGIN_NAME, LOGIN_EMAIL, LOGIN_PASSWORD, LOGIN_DATE, client)

    data = [{'name': 'яблоко', 'value': 100}, {'name': 'груша', 'value': 200}]
    diary = Diary()
    user_id = current_user.get_id()
    for products in data:
        product_name = products['name']
        grams = products['value']
        diary.add_product(product_name, grams, user_id)

    response = client.get('/profile')
    assert response.status_code == 200

    assert b'login_email@example.com' in response.data

    for i in range(2):
        diary = Diary.query.filter_by(user_id=current_user.get_id()).first()
        db.session.delete(diary)
        db.session.commit()
    logout(LOGIN_EMAIL)

#   72? , 90-134??, 158??, 196-210, 215-251,  265-266
