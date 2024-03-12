from flask import (
    render_template,
    request,
    redirect,
)
from flask_login import login_required, login_user, logout_user, current_user

from app import app, login_manager, db

from .UserLogin import UserLogin

from .models import Users


@login_manager.user_loader
def load_user(user_id):
    print("load user")
    return UserLogin().from_db(user_id)


@app.route("/")
def index():
    return "hello"


@app.route("/login", methods=["POST", "GET"])
def login():
    message = None
    if request.method == "POST":
        password = request.form["password"]
        email = request.form["email"]
        user = Users.query.filter_by(email=email, password=password).first_or_404() # ищем человека
        if user:
            user = UserLogin().create(user)
            login_user(user, remember=True)
            return redirect("/")
        else:
            message = "Неверное имя пользователя, email или пароль"
    context = {"message": message}
    return render_template("login.html", **context)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=5000)
