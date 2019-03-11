from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User, Post


class LoginForm(FlaskForm):  # base form FlaskForm is provided by wtforms
    #  static/class variables
    # somefield = SomeField("label_text", validators=[DataRequired()])
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    password_confirm = PasswordField("confirm password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(self, username):  # query the database to make sure username does not exist already
        hit = User.query.filter_by(username=username.data).first()
        if hit is not None:
            raise ValidationError("Please use a different username.")


    def validate_email(self, email):  # query database to make sure email does not exist already
        hit = User.query.filter_by(email=email.data).first()
        if hit is not None:
            raise ValidationError("Please use a different email.")

    # def validate_unique(self, model, **kwargs):  # abstract the first two methods to make code base simpler
    #     hit = model.query.filter_by(kwargs.data).first()
    #     return hit is None


# end forms
