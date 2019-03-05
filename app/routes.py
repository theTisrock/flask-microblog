from flask import render_template, flash, redirect, url_for
from flask_login import login_user
from app import app, login
from app.models import User, Post
from app.forms import LoginForm


@app.route("/")
@app.route("/index")
def index():
    user = {'username': "chris"}
    posts = [
        {
            'author' : {'username' : "John"},
            'body' : "One day I'll be an astronaut"
        },
        {
            'author' : {'username' : "Chris"},
            'body' : "I want to get into software development"
        }
    ]
    return render_template("index.html", title="Home", user=user, posts=posts)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()  # only works if username is unique.

        if user is not None and user.check_password(form.password.data):  # authenticate if result is returned
            login_user(user) # set the session

        else:  # if user not found in database or bad password
            flash("Invalid username or password.")
            return redirect(url_for('login'))

        return redirect(url_for('index'))
    return render_template("login.html", title="log in", form=form)
