import bcrypt
import pytest
import pandas as pd
from app import app, db
from .test import make_df_for_model
from .models import Users, QuestionsSleep
from flask_login import current_user, logout_user
from datetime import timedelta, date

LOGIN_EMAIL = "login_email@example.com"
LOGIN_NAME = "login_test_name"
LOGIN_PASSWORD = "login_test_password"
LOGIN_DATE = date.today() - timedelta(days=1)


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_questions_sleep():
    questions_sleep = QuestionsSleep(
        user_id=0,
        tofu="Нет",
        processed_meat="Нет",
        play_sport="Иногда",
        eat_weekend="Да, я больше ем дома",
        sleep_night="Хорошо",
        sugary_drinks=0,
        cows_milk="Да",
        fresh_cheeses="Да",
        miss_meals="Нет",
        vegetable_drinks="Иногда",
        eat_fast="Нет",
        cooked_vegetables="Да",
        low_fat_yogurt="Иногда",
        wake_up_eat_night="Никогда",
        hungry_during_day="Я всегда голоден",
        nuts="Да",
        fish="Никогда",
        fruits="Фрукты",
        eggs="Да",
        whole_grains_food="Каждый день",
        eat_uncontrollably="Никогда",
        alcoholic_beverages=0,
        meat="Часто с кем-то",
        sex="М",
    )
    return questions_sleep


def login(name, email, password, date_of_registration, client, mock_questions_sleep):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    new_user = Users(
        name=name,
        email=email,
        password=hashed_password.decode("utf-8"),
        date_of_registration=date_of_registration,
    )
    db.session.add(new_user)
    db.session.commit()
    user = Users.query.filter_by(email=email).first()
    questions = mock_questions_sleep
    questions.user_id = user.id
    db.session.add(questions)
    db.session.commit()
    response = client.post("/login", data={"email": email, "password": password})


def logout(email):
    user = Users.query.filter_by(email=email).first()
    answers = QuestionsSleep.query.filter_by(user_id=user.id).first()
    db.session.delete(answers)
    db.session.delete(user)
    db.session.commit()
    logout_user()


@pytest.fixture(scope="module")
def user_info():
    user = Users.query.filter_by(email=LOGIN_EMAIL).first()
    return user


def test_make_df_for_model_returns_list(mock_questions_sleep, client):
    login(
        LOGIN_NAME,
        LOGIN_EMAIL,
        LOGIN_PASSWORD,
        LOGIN_DATE,
        client,
        mock_questions_sleep,
    )
    user = Users.query.filter_by(email=LOGIN_EMAIL).first()
    questions = mock_questions_sleep
    questions.user_id = user.id
    result = make_df_for_model(current_user, questions)
    assert isinstance(result, list)
    assert len(result) == 2
    logout(LOGIN_EMAIL)


def test_make_df_for_model_first_element_is_dataframe(mock_questions_sleep, client):
    login(
        LOGIN_NAME,
        LOGIN_EMAIL,
        LOGIN_PASSWORD,
        LOGIN_DATE,
        client,
        mock_questions_sleep,
    )
    questions = mock_questions_sleep
    user = Users.query.filter_by(email=LOGIN_EMAIL).first()
    questions.user_id = user.id
    result = make_df_for_model(current_user, questions)
    assert isinstance(result[0], pd.DataFrame)
    logout(LOGIN_EMAIL)


def test_make_df_for_model_second_element_is_list(mock_questions_sleep, client):
    login(
        LOGIN_NAME,
        LOGIN_EMAIL,
        LOGIN_PASSWORD,
        LOGIN_DATE,
        client,
        mock_questions_sleep,
    )
    questions = mock_questions_sleep
    user = Users.query.filter_by(email=LOGIN_EMAIL).first()
    questions.user_id = user.id
    result = make_df_for_model(current_user, questions)
    assert isinstance(result[1], list)
    logout(LOGIN_EMAIL)


def test_make_df_for_model_dataframe_has_correct_columns(mock_questions_sleep, client):
    login(
        LOGIN_NAME,
        LOGIN_EMAIL,
        LOGIN_PASSWORD,
        LOGIN_DATE,
        client,
        mock_questions_sleep,
    )
    questions = mock_questions_sleep
    user = Users.query.filter_by(email=LOGIN_EMAIL).first()
    questions.user_id = user.id
    result = make_df_for_model(current_user, questions)
    expected_columns = [
        "Tofu_Don't_know",
        "Tofu_No",
        "Tofu_Sometimes",
        "Tofu_Yes",
        "Processed_Meat_es_prosciutto_No",
        "Processed_Meat_es_prosciutto_Sometimes",
        "Processed_Meat_es_prosciutto_Yes",
        "SEX_F",
        "SEX_M",
        "Do_you_play_a_sport_at_least_5_hours/week_No",
        "Do_you_play_a_sport_at_least_5_hours/week_Yes",
        "Do_you_eat_differently_at_the_weekend_I_cook_more_elaborate",
        "Do_you_eat_differently_at_the_weekend_No",
        "Do_you_eat_differently_at_the_weekend_Yes_I_eat_at_restaurants",
        "Do_you_eat_differently_at_the_weekend_Yes_I_eat_more_at_home",
        "Cow's_milk_No",
        "Cow's_milk_Sometimes",
        "Cow's_milk_Yes",
        "Fresh_cheeses_No",
        "Fresh_cheeses_Sometimes",
        "Fresh_cheeses_Yes",
        "Do_you_ever_miss_meals_No",
        "Do_you_ever_miss_meals_Yes",
        "Do_you_ever_miss_meals_Yes_breakfast",
        "Do_you_ever_miss_meals_Yes_dinner",
        "Do_you_ever_miss_meals_Yes_lunch",
        "Cooked_vegetables_No",
        "Cooked_vegetables_Sometimes",
        "Cooked_vegetables_Yes",
        "Low-fat_white_yogurt_No",
        "Low-fat_white_yogurt_Sometimes",
        "Low-fat_white_yogurt_Yes",
        "Do_you_wake_up_to_eat_at_night_Every_day",
        "Do_you_wake_up_to_eat_at_night_Infrequent_1/month",
        "Do_you_wake_up_to_eat_at_night_Never",
        "Do_you_wake_up_to_eat_at_night_Often_>1/week",
        "When_are_you_hungry_during_the_day_I'm_always_hungry",
        "When_are_you_hungry_during_the_day_In_the_afternoon",
        "When_are_you_hungry_during_the_day_In_the_evening",
        "When_are_you_hungry_during_the_day_In_the_morning",
        "When_are_you_hungry_during_the_day_afternoon+evening",
        "Nuts_No",
        "Nuts_Sometimes",
        "Nuts_Yes",
        "Fish_No",
        "Fish_Sometimes",
        "Fish_Yes",
        "Fruits_No",
        "Fruits_Sometimes",
        "Fruits_Yes",
        "Eggs_No",
        "Eggs_Sometimes",
        "Eggs_Yes",
        "Whole_grains_food_No",
        "Whole_grains_food_Sometimes",
        "Whole_grains_food_Yes",
        "Do_you_happen_to_eat_uncontrollably_even_if_you're_not_hungry_Every_day",
        "Do_you_happen_to_eat_uncontrollably_even_if_you're_not_hungry_Infrequent_1/month",
        "Do_you_happen_to_eat_uncontrollably_even_if_you're_not_hungry_Never",
        "Do_you_happen_to_eat_uncontrollably_even_if_you're_not_hungry_Often_>1/week",
        "Meat_No",
        "Meat_Sometimes",
        "Meat_Yes",
        "How_many_sugary_drinks_do_you_consume_per_day",
        "How_many_times_do_you_consume_alcoholic_beverages_in_a_week",
    ]
    assert result[0].columns.tolist() == expected_columns
    logout(LOGIN_EMAIL)
