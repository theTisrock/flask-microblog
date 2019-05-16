
# begin user authentication routes

# flask stuff
from flask import render_template, request, flash, url_for, redirect
# extensions
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from flask_babel import _
# my stuff
from microblog_app import db
from microblog_app.user_auth import bp
from microblog_app.urls import URLRoute
from microblog_app.models import User
from microblog_app.user_auth.email import send_password_reset_email
from microblog_app.user_auth.forms import LoginForm, RegistrationForm, PasswordResetRequestForm, ResetPasswordForm


@bp.route(URLRoute.login, methods=['GET', 'POST'])
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
            return redirect(url_for(Action.index, next=next_page))
        else:
            # invalid
            flash(_("Invalid username or password"))
            return redirect(url_for(Action.login))
    return render_template("login.html", title=_("Login"), form=form)


@bp.route(URLRoute.logout)
def logout():
    logout_user()  # clear the user session
    flash(_("Logged out"))
    return redirect(Action.login)


@bp.route(URLRoute.register, methods=['GET', 'POST'])
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
        flash(_(f"Registration success! Welcome {new_user.username}"))
        return redirect(url_for(Action.login))
    elif not registration_form.validate_on_submit() and request.method == 'POST':
        flash(_("Registration failed."))
        return render_template("register.html", title=_("Register"), form=registration_form)
    return "Error in register action"  # debugging


@bp.route(URLRoute.request_password_reset, methods=['GET', 'POST'])  # sends an email with a token
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for(Action.index))
    form = PasswordResetRequestForm()

    if form.validate_on_submit():  # give feedback to user
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            send_password_reset_email(user)
        flash(_(f"If this user exists, an email will be sent to {form.email.data}!"))
        return redirect(url_for(Action.login))

    return render_template("reset_password_request.html", title=_("Reset Password"), form=form)


@bp.route(URLRoute.reset_password, methods=['GET', 'POST'])  # performs the actual password reset
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for(Action.index))
    user = User.verify_reset_password_token(token)  # gets a user or returns None
    if not user:
        flash(_("User not found!"))
        return redirect(Action.register)
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_("Your password has been reset."))
        return redirect(url_for(Action.login))
    return render_template("reset_password.html", title=_("Reset Your Password"), form=form)

# end user authentication routes
