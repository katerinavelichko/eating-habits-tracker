import pytest
from app import app, db
from .models import Users
from flask_wtf import csrf


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


def test_soon(client):
    response = client.get('/soon')
    assert response.data == 'Скоро тут что-то будет'.encode('utf-8')


def test_login(client):
    response = client.post('/login', data={'email': 'invalid@example.com', 'password': 'invalidpassword'})
    assert 'Неверный email или пароль'.encode('utf-8') in response.data


def test_login_adds_user_to_database(client):
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


def test_tracker_form(client):
    response = client.get('/diary')
    assert response.status_code == 200


def test_surveys(client):
    response = client.get('/questions')
    assert response.status_code == 200


# @pytest.mark.parametrize("data, data1", [
#     (d, 4), (d, 2)
# ])
def test_create_user(client):
    response = client.get('/signup')
    assert response.status_code == 200

    csrf_token = csrf.generate_csrf()
    response = client.post('/signup',
                           data={'name': 'testname', 'email': 'valid_email@example.com', 'password': '12345678',
                                 'csrf_token': csrf_token})
    assert response.status_code == 302
    assert Users.query.filter_by(email='valid_email@example.com').first() is not None

    # response = client.post('/signup', data={'name': 'Test User', 'email': 'invalid_email', 'password': 'invalid'}, follow_redirects=True)
    # assert 'Некорректный email'.encode('utf-8') in response.data
    # assert Users.query.filter_by(email='invalid_email').first() is None
