import os
import secrets

from flask import current_app, url_for
from flask_mail import Message
from PIL import Image

from flaskblog import mail


def save_picture(form_picture):
    # names can collide
    random_hex = secrets.token_hex(8)
    # retain file extension
    # _ could be f_name if wanted the file name, _ throws away the variable (or get unused variable)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # root path is our application all the way up to the package directory (including)
    picture_path = os.path.join(
        current_app.root_path, "static/profile_pics", picture_fn
    )

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    # msg = Message("Password Reset Request", sender="jason.wallenfang@comcast.net", )
    msg = Message(
        "Password Reset Request", sender="noreply@demo.com", recipients=[user.email]
    )
    # only use 1 "{" since using an f string
    # _external=True generates a full URL (not relative)
    msg.body = f"""To reset you password, visit the following link:
{url_for("users.reset_token", token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
"""
    mail.send(msg)
