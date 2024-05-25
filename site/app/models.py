from . import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from .test import search_images

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))
    date_of_registration = db.Column(db.Date)

    @classmethod
    def add_user(cls, name, email, password):
        user = cls(name=name, email=email, password=password, date_of_registration=date.today())
        db.session.add(user)
        db.session.commit()
        print(f'Добавлен новый пользователь: {name}')

    @classmethod
    def delete_user(cls, name, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            print(f'Пользователь {name} был удален')
        else:
            print(f'Пользователя {name} нет в списках')


class QuestionsSleep(db.Model):
    __tablename__ = 'questions_sleep'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tofu = db.Column(db.String(255))
    processed_meat = db.Column(db.String(255))
    play_sport = db.Column(db.String(255))
    eat_weekend = db.Column(db.String(255))
    sleep_night = db.Column(db.String(255))
    sugary_drinks = db.Column(db.String(255))
    cows_milk = db.Column(db.String(255))
    fresh_cheeses = db.Column(db.String(255))
    miss_meals = db.Column(db.String(255))
    vegetable_drinks = db.Column(db.String(255))
    eat_fast = db.Column(db.String(255))
    cooked_vegetables = db.Column(db.String(255))
    low_fat_yogurt = db.Column(db.String(255))
    wake_up_eat_night = db.Column(db.String(255))
    hungry_during_day = db.Column(db.String(255))
    nuts = db.Column(db.String(255))
    fish = db.Column(db.String(255))
    fruits = db.Column(db.String(255))
    eggs = db.Column(db.String(255))
    whole_grains_food = db.Column(db.String(255))
    eat_uncontrollably = db.Column(db.String(255))
    alcoholic_beverages = db.Column(db.String(255))
    meat = db.Column(db.String(255))
    sex = db.Column(db.String(10))

    @classmethod
    def add_question(cls, user_id, question_data):
        question_data['user_id'] = user_id
        question = cls(**question_data)
        db.session.add(question)
        db.session.commit()
        print(f'Добавлен новый вопрос')


class Diary(db.Model):
    __tablename__ = 'diary'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_name = db.Column(db.String(200))
    grams = db.Column(db.Integer)
    date = db.Column(db.Date)

    @classmethod
    def add_product(cls, product_name, grams, user_id):
        today = date.today()
        product = cls(user_id=user_id, product_name=product_name, grams=grams, date=today)
        db.session.add(product)
        db.session.commit()

    @classmethod
    def get_products_today(cls, user_id, cur_date):
        products = cls.query.filter_by(user_id=user_id, date=cur_date).all()
        products_list = []
        for product in products:
            product_dict = {
                'product_name': product.product_name,
                'grams': product.grams
            }
            products_list.append(product_dict)
        return products_list


class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Text)
    title = db.Column(db.String(255))
    description = db.Column(db.String(500))
    tags = db.Column(db.String(500))
    date_of_post = db.Column(db.Date)
    photo = db.Column(db.String(500))

    @classmethod
    def add_post(cls, text, title, description, tags, user_id):
        today = date.today()
        photo = search_images(tags.split(', ')[0])
        print(search_images(tags.split(', ')[0]))
        post = cls(user_id=user_id, text=text, title=title, description=description, tags=tags, date_of_post=today, photo=photo)
        db.session.add(post)
        db.session.commit()

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    text = db.Column(db.Text)
    date_of_comment = db.Column(db.Date)

    @classmethod
    def add_comment(cls, text, post_id, user_id):
        today = date.today()
        comment = cls(user_id=user_id, text=text, post_id=post_id, date_of_comment=today)
        db.session.add(comment)
        db.session.commit()