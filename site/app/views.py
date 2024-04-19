import json

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    jsonify
)
from flask_login import login_required, login_user, logout_user, current_user
from app import app, login_manager, db
from yandexgptlite import YandexGPTLite

from .UserLogin import UserLogin
from .forms import CreateUserForm
from .models import Users, QuestionsSleep
from .test import make_df_for_model

from joblib import load
from sklearn.ensemble import RandomForestClassifier
import os
import constants
import requests

current_directory = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_directory, 'rf_model.joblib')

# Load the model
rf_model = load(model_path)


@login_manager.user_loader
def load_user(user_id):
    print("load user")
    return UserLogin().from_db(user_id)


@app.route("/")
def index():
    return render_template("main.html")


@app.route("/soon")
def soon():
    return "Скоро тут что-то будет"


@app.route("/login", methods=["POST", "GET"])
def login():
    message = None
    if request.method == "POST":
        password = request.form["password"]
        email = request.form["email"]
        user = Users.query.filter_by(email=email, password=password).first()  # ищем человека
        if user:
            user = UserLogin().create(user)
            login_user(user, remember=True)
            return redirect("/")
        else:
            message = "Неверный email или пароль"
            context = {"message": message}
            return render_template("login.html", **context)
    context = {"message": message}
    return render_template("login.html", **context)


@app.route("/questions")
@login_required
def surveys():
    return render_template("surveys.html")


@app.route("/profile")
@login_required
def profile():
    user_id = current_user.get_id()
    user = Users.query.get(user_id)
    context = {
        'user': user
    }
    return render_template("profile.html", **context)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


@app.route("/signup", methods=["GET", "POST"])
def create_user():
    message = None
    form = CreateUserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if not Users.query.filter_by(email=form.email.data).first():
                email = form.email.data
                name = form.name.data
                password = form.password.data
                Users.add_user(name, email, password)
                return redirect(url_for("index"))
            else:
                return redirect(url_for("unsuccess"))
        else:
            message = "Некорректный email"
    context = {
        "message": message,
    }
    return render_template("form_users.html", form=form, **context)


@app.route("/receive_data", methods=["POST", "GET"])
@login_required
def receive_data_from_forms():
    data = request.get_json()

    form = QuestionsSleep()

    user_id = current_user.get_id()
    form.add_question(user_id, data)
    return data


@app.route("/profile/answers", methods=["GET", "POST"])
@login_required
def answers():
    number = rf_model.predict(make_df_for_model(current_user, QuestionsSleep)[0]).tolist()[0]
    keys = make_df_for_model(current_user, QuestionsSleep)[1]
    if int(number) == 1:
        prompt = "Напиши в стиле наставления мне, что у меня хорошее качество сна, но чтобы его улучшить, нужно исправить 3 критерия:" + \
                 keys[0] + "," + keys[1] + "," + keys[2]
    else:
        prompt = "Напиши в стиле наставления мне, что у меня плохое качество сна, и чтобы его улучшить, нужно исправить 3 критерия:" + \
                 keys[0] + "," + keys[1] + "," + keys[2]
    account = YandexGPTLite('b1gcghjsok0u7pp94plu', 'y0_AgAEA7qkP0WqAATuwQAAAAEAKm7pAABo1V6HejhPmpns95QMCEdmlEb2QA')
    text = account.create_completion(prompt, '0.6')
    text1 = ''.join(text.split(":")[1:])
    return text1


@app.route("/profile/tracker")
def tracker():
    api_key = '0YxRi3d18MNz4gCrOT7ROtD0rTMu94TyKsvc9XBQ'
    search_query = 'apple strudel'
    g = 200
    context = {}
    url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={search_query}'

    response = requests.get(url)

    nutrients = {'Energy': 0, 'Protein': 0, 'Total lipid (fat)': 0, 'Carbohydrate, by difference': 0,
                 'Fiber, total dietary': 0, 'Total Sugars': 0}
    units = {'Energy': 'kcal', 'Protein': 'g', 'Total lipid (fat)': 'g', 'Carbohydrate, by difference': 'g',
             'Fiber, total dietary': 'g', 'Total Sugars': 'g'}

    if response.status_code == 200:
        data = response.json()
        for nutrient in data['foods'][0]['foodNutrients']:
            if nutrient['nutrientName'] in nutrients.keys():
                nutrients[nutrient['nutrientName']] = nutrient['value']
        for key in nutrients.keys():
            context[key.replace(' ', '').replace(',', '').replace('(', '').replace(')', '')] = [key, format(
                nutrients[key] / 100 * g, '.2f'), units[key]]
    else:
        print('Ошибка при запросе к API:', response.status_code)
    return render_template("tracker.html", **context)


# @app.route("/signup/success")
# def success():
#     return render_template("success.html")
#
#
@app.route("/signup/unsuccess")
def unsuccess():
    return render_template("unsuccess.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=5000)
