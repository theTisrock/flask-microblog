from microblog_app import app  # importing the Flask object called "app" in __init__.py
from microblog_app.forms import LoginForm
from microblog_app.models import User, Post
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user


@app.route("/")
@app.route("/index")
def index():
    user = {'username':"miguel"}
    posts = [
        {
            'author': {'username': "John"},
            'body': "It's such a beautiful day"
        },
        {
            'author': {'username': "Susan"},
            'body': "Susan's first blog!"
        }
    ]
    return  render_template("index.html", title="Home", user=user, posts=posts)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # current user is either authenticated or anonymous
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            # valid
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        else:
            # invalid
            flash("Invalid username or password")
            return redirect(url_for('login'))
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()  # clear the user session
    return redirect(url_for("login"))

# end routes
