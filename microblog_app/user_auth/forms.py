
# begin user authentication forms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
from microblog_app.models import User
from flask_babel import _, lazy_gettext as _l


class LoginForm(FlaskForm):
    # more than one validator can be assigned to a field in a list
    # username = StringField("label", validators=[] )
    username = StringField(_l("Username"), validators=[DataRequired()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    remember_me = BooleanField(_l("Remember Me"))
    submit = SubmitField(_l("Submit"))


class RegistrationForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired()])
    email = StringField(_l("Email"), validators=[DataRequired(), Email(), Length(min=5, max=120)])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    confirm_password = PasswordField(_l("Confirm Password"), validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField(_l("Register"))

    # custom validators passed to framework: validate_field(self, field_object)
    # these are called at request time, not at module parse time
    def validate_username(self, username):  # if that user does not exist, its valid. user must be unique.
        found_user = User.query.filter_by(username=username.data).first()
        if found_user:
            raise ValidationError(_("Please use a different username."))

    def validate_email(self, email):
        found_email = User.query.filter_by(email=email.data).first()
        if found_email:
            raise ValidationError(_("Please use a different email."))


class PasswordResetRequestForm(FlaskForm):
    email = StringField(_l("email"), validators=[DataRequired(), Email()])
    submit = SubmitField(_l("Reset Password"))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    confirm_password = PasswordField(_l("Confirm Password"), validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField(_l("Save New Password"))

# end user authentication forms
