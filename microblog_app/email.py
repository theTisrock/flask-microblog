
# begin generic emails

from threading import Thread
from microblog_app import mail
from flask_mail import Message
from flask import current_app


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)  # send via smtp


def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    # separate thread to send emails
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

# end generic emails
