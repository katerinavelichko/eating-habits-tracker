from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from . import views
import os

app = Flask(__name__)
DEBUG = True
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL',
                                                       'postgresql://experimentals:experimentals1@db:5432/habits_db')

# DataBase
db = SQLAlchemy(app)
migrate = Migrate(app, db)