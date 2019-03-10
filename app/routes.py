from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app.models import User, Post
from app.forms import LoginForm


@app.route("/")
@app.route("/index")
@login_required
def index():
    # test data
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
    return render_template("index.html", title="Home", posts=posts)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # reroute the logged in user to index
        redirect(url_for("index"))
    form = LoginForm()
    after_login = request.args.get('next')  # returns next query string or None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()  # only works if username is unique.

        if user is not None and user.check_password(form.password.data):  # authenticate if result is returned
            login_user(user, remember=form.remember_me.data)  # set the session. remember is optional arg.

            if not after_login or url_parse(after_login).netloc != "":
                after_login = url_for("index")

        else:  # if user not found in database or bad password
            flash("Invalid username or password.")  # implemented "need to know" basis security.
            return redirect(url_for("login"))

        return redirect(after_login)
    return render_template("login.html", title="log in", form=form)


@app.route("/logout")
def logout():
    logout_user()  # clears the user session
    return redirect(url_for("index"))

