
# begin main or generic routes

# flask stuff
from flask import render_template, request, flash, url_for, redirect, current_app, jsonify, g
# extensions
from flask_login import current_user, login_required
from flask_babel import get_locale
from guess_language import guess_language
from flask_babel import _
# my stuff
from microblog_app import db
from microblog_app.translate import translate
from microblog_app.main import bp
from microblog_app.main.forms import EditProfileForm, BlogPostForm
from microblog_app.models import User, Post
from microblog_app.urls import URLRoute, Action


@bp.app_context_processor
def load_context():
    actions = {
        'user': Action.user, 'edit_profile': Action.edit_profile, 'explore': Action.explore,
        'index': Action.index, 'login': Action.login, 'logout': Action.logout, 'register': Action.register
    }
    return dict(
        Actions=actions
    )


@bp.before_request  # applies to all routes in the application
def before_request():
    if current_user.is_authenticated:
        current_user.timestamp_on_request()
    g.locale = str(get_locale())  # g is a static field that can hold data and is accessible between request points


@bp.route(URLRoute.edit_profile, methods=['GET', 'POST'])  # edit profile
@login_required
def edit_profile():
    edit_profile_form = EditProfileForm(current_user.username)

    if edit_profile_form.validate_on_submit() and request.method == 'POST':  # accept changes
            current_user.username = edit_profile_form.username.data
            current_user.about_me = edit_profile_form.about_me.data
            db.session.commit()
            flash(_(f"Saved changes to \"About Me\" section for {current_user.username}"))

    elif request.method == 'GET':  # pre-populate current state of 'About me' section
        edit_profile_form.username.data = current_user.username
        edit_profile_form.about_me.data = current_user.about_me

    return render_template("edit_profile.html", title="Edit Profile", form=edit_profile_form)


@bp.route(URLRoute.explore)
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )
    next_page = url_for(Action.explore, page=posts.next_num) if posts.has_next else None
    prev_page = url_for(Action.explore, page=posts.prev_num) if posts.has_prev else None
    return render_template("index.html", title="explore", blog_form=None, posts=posts.items,
                           next_page=next_page, prev_page=prev_page)


# index
@bp.route(URLRoute.home['root'], methods=['GET', 'POST'])  # app decorators first
@bp.route(URLRoute.home['index'], methods=['GET', 'POST'])
@login_required  # then login decorators
def index():
    form = BlogPostForm()

    if form.validate_on_submit() and request.method == 'POST':
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:  # if lang isn't determined correctly
            language = ''  # void the language
        new_post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(new_post)
        db.session.commit()
        flash(_("You're post is now live!"))
        return redirect(url_for(Action.index))

    page = request.args.get('page', 1, type=int)  # access the query string. get('key', default, type)

    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False  # 3rd arg prevents 404 result
    )

    next_page = url_for(Action.index, page=posts.next_num) if posts.has_next else None
    prev_page = url_for(Action.index, page=posts.prev_num) if posts.has_prev else None

    return render_template("index.html", title=_("Home"), blog_form=form, posts=posts.items,
                           next_page=next_page, prev_page=prev_page)


# user
@bp.route(URLRoute.user)
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()  # returns either element or 404 response
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )
    next_page = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_page = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template("user.html", title=_(f"{user.username}'s profile"), user=user, posts=posts.items,
                           next_page=next_page, prev_page=prev_page)


@bp.route(URLRoute.follow)
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:  # if user is not found in db
        flash(_(f"User {username} was not found."))
        return redirect(url_for(Action.index))
    elif user is not None and current_user == user:  # if user is found && the user is yourself
        flash(_(f"You cannot follow yourself."))
        return redirect(url_for(Action.user, username=username))
    else:  # valid user
        current_user.follow(user)
        db.session.commit()
        flash(_(f"You are now following {username}"))
        return redirect(url_for(Action.user, username=username))


@bp.route(URLRoute.unfollow)
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_(f"User {username} was not found."))
        return redirect(url_for(Action.index))
    elif user is not None and current_user == user:
        flash(_(f"You cannot unfollow yourself."))
        return redirect(url_for(Action.user, username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_(f"You unfollowed {username}"))
    return redirect(url_for(Action.user, username=username))


@bp.route("/translate", methods=['POST'])
@login_required
def translate_text():
    # wtf not used here. Instead, the flask request object is used. No web form needed. Just use request.form dictionary
    return jsonify({
        'text': translate(
            request.form['text'],
            request.form['source_language'],
            request.form['dest_language'])
        })

# idea: build a class of urls and corresponding action names. Less fragile.
# I would only have to change action names in class instead of strings in every route, redirect, or url_for() call

# end main/generic routes
