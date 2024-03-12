import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopementConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL', 'postgresql://experimentals:experimentals1@db:5432/habits_db')