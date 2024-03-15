from .models import Users
from flask_login import UserMixin


class UserLogin(UserMixin):
    def __init__(self):
        self.__user = None

    def from_db(self, user_id):
        self.__user = Users.query.get(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user.id)

    def get_user(self, user_id):
        self.__user = Users.query.get(user_id)
        return self
