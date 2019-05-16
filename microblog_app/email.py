
# begin generic emails

from threading import Thread
from microblog_app import mail, app
from flask_mail import Message
from flask import render_template
from flask_babel import _


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)  # send via smtp


def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    Thread(target=send_async_email, args=(app, msg)).start()  # separate thread to send emails

# end generic emails
