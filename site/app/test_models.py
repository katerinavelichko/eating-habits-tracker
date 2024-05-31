import pytest
from .models import Users, QuestionsSleep, Diary, Posts, Comment
from datetime import date
from app import app, db


@pytest.fixture(scope="module")
def new_question_data():
    return {
        "sex": "М",
        "tofu": "Да",
        "fresh_cheeses": "Да",
        "processed_meat": "Нет",
        "play_sport": "Да",
        "eat_weekend": "Да, я ем в ресторанах",
        "sugary_drinks": 3,
        "cows_milk": "Иногда",
        "miss_meals": "Нет",
        "vegetable_drinks": "Да",
        "eat_fast": "Да",
        "cooked_vegetables": "Иногда",
        "low_fat_yogurt": "Да",
        "wake_up_eat_night": "Нечасто (около 1-го раза в месяц)",
        "alcoholic_beverages": 2,
        "eat_uncontrollably": "Нечасто (около 1-го раза в месяц)",
        "whole_grains_food": "Да",
        "eggs": "Да",
        "fruits": "Да",
        "fish": "Да",
        "meat": "Да",
        "nuts": "Да",
        "hungry_during_day": "Днем",
    }


@pytest.fixture(scope="module")
def new_diary_product():
    return {"product_name": "яблоко", "grams": 100}


@pytest.fixture(scope="module")
def new_user():
    user = Users(
        name="Test User", email="test_user@example.com", password="test_password"
    )
    Users.add_user(user.name, user.email, user.password)
    return user


@pytest.fixture(scope="module")
def user_info():
    user = Users.query.filter_by(email="test_user@example.com").first()
    return user


@pytest.fixture(scope="module")
def new_diary_product(user_info):
    return {"product_name": "яблоко", "grams": 100, "user_id": user_info.id}


@pytest.fixture(scope="module")
def new_post(user_info):
    return {
        "text": "post text",
        "title": "post title",
        "description": "post description",
        "tags": "test, post",
        "user_id": user_info.id,
    }


@pytest.fixture(scope="module")
def post_info(user_info):
    post = Posts.query.filter_by(user_id=user_info.id).first()
    return post


@pytest.fixture(scope="module")
def new_comment(post_info):
    return {
        "text": "comment text",
        "post_id": post_info.id,
        "user_id": post_info.user_id,
    }


def test_add_user(new_user):
    assert new_user.name == "Test User"
    assert new_user.email == "test_user@example.com"


def test_add_question(user_info, new_question_data):
    question_cnt = QuestionsSleep.query.filter_by(user_id=user_info.id).count()
    QuestionsSleep.add_question(user_info.id, new_question_data)
    final_question_cnt = QuestionsSleep.query.filter_by(user_id=user_info.id).count()

    assert final_question_cnt == question_cnt + 1

    question = QuestionsSleep.query.filter_by(user_id=user_info.id).first()
    db.session.delete(question)
    db.session.commit()


def test_add_diary_product(user_info, new_diary_product):
    product_cnt = Diary.query.filter_by(user_id=user_info.id).count()
    Diary.add_product(**new_diary_product)
    final_prodct_cnt = Diary.query.filter_by(user_id=user_info.id).count()

    assert final_prodct_cnt == product_cnt + 1

    prdct = (
        Diary.query.filter_by(user_id=user_info.id).order_by(Diary.id.desc()).first()
    )

    assert prdct.product_name == new_diary_product["product_name"]
    assert prdct.grams == new_diary_product["grams"]

    diary_entry = Diary.query.filter_by(user_id=user_info.id).first()
    if diary_entry:
        db.session.delete(diary_entry)
        db.session.commit()


def test_add_post(new_post):
    post_cnt = Posts.query.filter_by(user_id=new_post["user_id"]).count()
    Posts.add_post(**new_post)
    final_post_cnt = Posts.query.filter_by(user_id=new_post["user_id"]).count()

    assert final_post_cnt == post_cnt + 1

    pst = (
        Posts.query.filter_by(user_id=new_post["user_id"])
        .order_by(Posts.id.desc())
        .first()
    )

    assert pst.text == new_post["text"]
    assert pst.title == new_post["title"]
    assert pst.description == new_post["description"]
    assert pst.tags == new_post["tags"]


def test_add_comment(new_comment):
    comm_cnt = Comment.query.filter_by(post_id=new_comment["post_id"]).count()
    Comment.add_comment(**new_comment)
    final_comm_cnt = Comment.query.filter_by(post_id=new_comment["post_id"]).count()

    assert final_comm_cnt == comm_cnt + 1

    cmnt = (
        Comment.query.filter_by(post_id=new_comment["post_id"])
        .order_by(Comment.id.desc())
        .first()
    )
    assert cmnt.text == new_comment["text"]

    comment = Comment.query.filter_by(post_id=new_comment["post_id"]).first()
    if comment:
        db.session.delete(comment)
        db.session.commit()

    post = Posts.query.filter_by(id=new_comment["post_id"]).first()
    if post:
        db.session.delete(post)
        db.session.commit()


def test_delete_user(user_info):
    Users.delete_user(user_info.name, user_info.email)
    user = Users.query.filter_by(email=user_info.email).first()

    assert user is None
