from microblog_app import app, db  # importing the Flask object called "app" in __init__.py
from microblog_app.forms import LoginForm, RegistrationForm, EditProfileForm, BlogPostForm
from microblog_app.models import User, Post
from microblog_app.urls import Action,URLRoute
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlite3.dbapi2 import IntegrityError


@app.before_request  # applies to all routes in the application
def before_request():
    if current_user.is_authenticated:
        current_user.timestamp_on_request()


# edit profile
@app.route(URLRoute.edit_profile, methods=['GET', 'POST'])
@login_required
def edit_profile():
    edit_profile_form = EditProfileForm(current_user.username)

    if edit_profile_form.validate_on_submit() and request.method == 'POST':  # accept changes
            current_user.username = edit_profile_form.username.data
            current_user.about_me = edit_profile_form.about_me.data
            db.session.commit()
            flash(f"Saved changes to \"About Me\" section for {current_user.username}")

    elif request.method == 'GET':  # pre-populate current state of 'About me' section
        edit_profile_form.username.data = current_user.username
        edit_profile_form.about_me.data = current_user.about_me

    return render_template("edit_profile.html", title="Edit Profile", form=edit_profile_form)


@app.route(URLRoute.explore)
@login_required
def explore():
    posts = Post.get_posts()
    return render_template("index.html", title="explore", blog_form=None, posts=posts)


# index
@app.route(URLRoute.home['root'], methods=['GET', 'POST'])  # app decorators first
@app.route(URLRoute.home['index'], methods=['GET', 'POST'])
@login_required  # then login decorators
def index():
    form = BlogPostForm()

    if form.validate_on_submit() and request.method == 'POST':
        new_post = Post(body=form.post.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash("You're post is now live!")
        return redirect(url_for(Action.index))

    posts = Post.get_posts()

    return render_template("index.html", title="Home", blog_form=form, posts=posts)


# login
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


# logout
@app.route(URLRoute.logout)
def logout():
    logout_user()  # clear the user session
    return redirect(Action.login)


# register
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


# user
@app.route(URLRoute.user)
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()  # returns either element or 404 response
    posts = Post.get_posts(filter_attr="user_id", filter_arg=user.id)
    return render_template("user.html", user=user, posts=posts)


@app.route(URLRoute.follow)
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:  # if user is not found in db
        flash(f"User {username} was not found.")
        return redirect(url_for(Action.index))
    elif user is not None and current_user == user:  # if user is found && the user is yourself
        flash(f"You cannot follow yourself.")
        return redirect(url_for(Action.user, username=username))
    else:  # valid user
        current_user.follow(user)
        db.session.commit()
        flash(f"You are now following {username}")
        return redirect(url_for(Action.user, username=username))


@app.route(URLRoute.unfollow)
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f"User {username} was not found.")
        return redirect(url_for(Action.index))
    elif user is not None and current_user == user:
        flash(f"You cannot unfollow yourself.")
        return redirect(url_for(Action.user, username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f"You unfollowed {username}")
    return redirect(url_for(Action.user, username=username))


# idea: build a class of urls and corresponding action names. Less fragile.
# I would only have to change action names in class instead of strings in every route, redirect, or url_for() call


# end routes
