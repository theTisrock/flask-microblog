
# begin main forms

# flask
from flask import request
# extensions
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
from flask_babel import _, lazy_gettext as _l
# my stuff
from microblog_app.models import User, Post


class BlogPostForm(FlaskForm):
    post = TextAreaField(_l("...say something..."), validators=[DataRequired(), Length(min=1, max=140, message="Hello")])
    submit = SubmitField(_l("publish live"))


class EditProfileForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired()])
    about_me = TextAreaField(_l("About Me"), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l("Save Changes"))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            found_user = User.query.filter_by(username=username.data).first()
            if found_user is not None:
                raise ValidationError(_("Please use a different username"))


class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])  # query

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'), validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))

# end main forms
