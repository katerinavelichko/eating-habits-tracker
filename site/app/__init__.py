from flask import Flask
import os


app = Flask(__name__)
DEBUG = True
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL', 'postgresql://experimentals:experimentals1@db:5432/habits_db')


from . import views