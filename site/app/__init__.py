import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
DEBUG = True
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL',
                                                       'postgresql://experimentals:experimentals1@db:5432/habits_db')

# DataBase
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
app.app_context().push()

from . import views