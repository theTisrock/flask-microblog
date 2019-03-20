from microblog_app import app, db  # importing the Flask object called "app" in __init__.py
from microblog_app.forms import LoginForm, RegistrationForm
from microblog_app.models import User, Post
from microblog_app.urls import Action,URLRoute
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.before_request  # applies to all routes in the application
def before_request():
    if current_user.is_authenticated:
        current_user.timestamp_on_request()


@app.route(URLRoute.home['root'])  # app decorators first
@app.route(URLRoute.home['index'])
@login_required  # then login decorators
def index():
    user = User.query.filter_by(username=current_user.username).first()
    posts = posts = [
        {'author': user, 'body': "Test blog #1"},
        {'author': user, 'body': "Test blog #2"}
    ]
    return render_template("index.html", title="Home", posts=posts)


@app.route(URLRoute.login, methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # current user is either authenticated or anonymous
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            # valid
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next') or Action.index  # landing page after login
            if url_parse(next_page).netloc != "":  # security if the domain has been modified
                return redirect(url_parse('index'))
            return redirect(url_for(next_page))
        else:
            # invalid
            flash("Invalid username or password")
            return redirect(url_for(Action.login))
    return render_template("login.html", title="Login", form=form)


@app.route(URLRoute.logout)
def logout():
    logout_user()  # clear the user session
    return redirect(Action.login)


@app.route(URLRoute.register, methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for(Action.login))  # redirect if logged in
    elif request.method == 'GET' and current_user.is_anonymous:
        return render_template("register.html", form=registration_form)  # display form if not logged in
    elif request.method == 'POST' and registration_form.validate_on_submit():
        # check that username, email are unique (don't exist in db yet)
            # this is already done by flask-wtf in User model class, most likely when validate_on_submit() is called
        # if form data not unique, flash error to user and reload "register.html", be ambiguous for security
        # if form data unique, add user to database, inform them they have successfully registered
        # all checks specified in this comment block are taken care of by flask-wtf custome validate_field() methods
        # ...so just add a user
        new_user = User(username=registration_form.username.data, email=registration_form.email.data)
        new_user.set_password(registration_form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Registration success! Welcome {new_user.username}")
        return redirect(url_for(Action.login))
    elif not registration_form.validate_on_submit() and request.method == 'POST':
        flash("Registration failed.")
        return render_template("register.html", form=registration_form)
    return "Error in register action"  # debugging


@app.route(URLRoute.user)
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()  # returns either element or 404 response
    posts = [
        {'author': user, 'body': "Test blog #1"},
        {'author': user, 'body': "Test blog #2"}
    ]
    return render_template("user.html", user=user, posts=posts)


# idea: build a class of urls and corresponding action names. Less fragile.
# I would only have to change action names in class instead of strings in every route, redirect, or url_for() call


# end routes
