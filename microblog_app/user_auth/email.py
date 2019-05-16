
# begin user authentication emails
from flask import render_template, current_app
from microblog_app.email import send_email
from flask_babel import _


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('[Microblog] Reset Your Password'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token))


# end user auth emails
