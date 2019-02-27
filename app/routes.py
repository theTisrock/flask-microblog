from flask import render_template, flash, redirect, url_for
from app import app
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
        flash("Login requested for {}, remember me = {}".format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))  # redirect looks for flash messages to load on the next screen
    return render_template("login.html", title="log in", form=form)
