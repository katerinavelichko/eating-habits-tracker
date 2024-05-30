import pytest
from .UserLogin import UserLogin
from .models import Users, QuestionsSleep, Diary


@pytest.fixture
def mock_user():
    user = Users(id=10, name="Test User")
    return user

@pytest.fixture
def class_instance(mock_user):
    instance = UserLogin()
    instance.__user = mock_user
    return instance

def test_from_db_returns_self(class_instance, mock_user):
    result = class_instance.from_db(user_id=10)
    assert result is class_instance

def test_from_db_sets_user_attribute(class_instance, mock_user):
    class_instance.from_db(user_id=10)
    assert class_instance.__user == mock_user

def test_get_user_returns_self(class_instance):
    result = class_instance.get_user(user_id=10)
    assert result is class_instance

def test_get_user_sets_user_attribute(class_instance, mock_user):
    class_instance.get_user(user_id=10)
    assert class_instance.__user == mock_user
