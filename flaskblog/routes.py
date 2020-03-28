import os
import secrets

# url_for: finds the exact location of routes for us, so we don't need to worry about it in the background
from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image

from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import (
    LoginForm,
    PostForm,
    RegistrationForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
)
from flaskblog.models import Post, User
from flaskblog.database import db_check, db_initialize
from flask_mail import Message


# route is used to navigate to different pages
@app.route("/")
def greeting():
    name = request.args.get("name", "World")
    return f"<h1>Hello, {escape(name)}!</h1><p>homepage</p>"


@app.route("/home")
def home():
    # posts = Post.query.all()
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # on the url when redirected to login from another page (url encoded)
            next_page = request.args.get("next")
            # python version of C++ ternary: x > 0 ? true : false;
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash(f"Login failed. Please check email and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


def save_picture(form_picture):
    # names can collide
    random_hex = secrets.token_hex(8)
    # retain file extension
    # _ could be f_name if wanted the file name, _ throws away the variable (or get unused variable)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # root path is our application all the way up to the package directory (including)
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.image_file = save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account updated.", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    # image_file is from models.py (User)
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash("Post created.", "success")
        return redirect(url_for("home"))
    return render_template(
        "create_post.html", title="New Post", form=form, legend="New Post"
    )


@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    # post = Post.query.get(post_id)
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # 403 forbidden
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post updated.", "success")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        "create_post.html", title="Update Post", form=form, legend="Update Post"
    )


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # 403 forbidden
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted.", "success")
    return redirect(url_for("home"))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.posted.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("user_posts.html", posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    # msg = Message("Password Reset Request", sender="jason.wallenfang@comcast.net", )
    msg = Message(
        "Password Reset Request", sender="noreply@demo.com", recipients=[user.email]
    )
    # only use 1 "{" since using an f string
    # _external=True generates a full URL (not relative)
    msg.body = f"""To reset you password, visit the following link:
{url_for("reset_token", token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
"""
    mail.send(msg)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    # make sure user is logged out first
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email was sent with instructions to reset your password.", "info")
        return redirect(url_for("login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    # make sure user is logged out first
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    # if not user (same as) if user is None
    if user is None:
        flash("Invalid or expired token", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash(f"Password has been updated.", "success")
        return redirect(url_for("login"))
    return render_template("reset_token.html", title="Reset Password", form=form)


# https://flask.palletsprojects.com/en/1.1.x/cli/
# import click
# @click.command('initdb')
@app.cli.command("initdb")
def initialize_db():
    """ Reinitialize the database and preload """
    db_initialize()
    return


# import click
# @click.command('check')
@app.cli.command("check")
def check_db():
    db_check()
    return
