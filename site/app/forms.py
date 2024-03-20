from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email, Length, DataRequired


class CreateUserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[Email(message="Invalid email address")])
    password = PasswordField(
        "Password", validators=[Length(min=8, message="Short password! min - 8")]
    )
    submit = SubmitField("Отправить")





