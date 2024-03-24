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

from .UserLogin import UserLogin
from .forms import CreateUserForm
from .models import Users, QuestionsSleep
from .test import make_df_for_model


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
                return redirect(url_for("success"))
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
    return render_template('answers.html')


# @app.route("/signup/success")
# def success():
#     return render_template("success.html")
#
#
# @app.route("/signup/unsuccess")
# def unsuccess():
#     return render_template("unsuccess.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=5000)
