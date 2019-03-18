from microblog_app import app  # importing the Flask object called "app" in __init__.py
from microblog_app.forms import LoginForm
from flask import render_template, flash, redirect, url_for, request


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
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash(f"Logged in user {form.username.data}, rememember_me={form.remember_me.data}")
        return redirect("/index")
    return render_template("login.html", title="Login", form=form)

# end routes
