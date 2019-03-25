# forms

from flask_wtf import FlaskForm
# flask-wtf uses wtforms as a dependency
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
from microblog_app.models import User, Post


class LoginForm(FlaskForm):
    # more than one validator can be assigned to a field in a list
    # username = StringField("label", validators=[] )
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Submit")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(min=5, max=120)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    # custom validators passed to framework: validate_field(self, field_object)
    def validate_username(self, username):  # if that user does not exist, its valid. user must be unique.
        found_user = User.query.filter_by(username=username.data).first()
        if found_user:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        found_email = User.query.filter_by(email=email.data).first()
        if found_email:
            raise ValidationError("Please use a different email.")


class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About Me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Save Changes")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            found_user = User.query.filter_by(username=username.data).first()
            if found_user is not None:
                raise ValidationError("Please use a different username")

# end forms
