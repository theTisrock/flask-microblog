# forms

from flask_wtf import FlaskForm
# flask-wtf uses wtforms as a dependency
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    # more than one validator can be assigned to a field in a list
    # username = StringField("label", validators=[] )
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("submit")

# end forms
