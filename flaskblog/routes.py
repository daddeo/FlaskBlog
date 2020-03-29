# import os
# import secrets
# url_for: finds the exact location of routes for us, so we don't need to worry about it in the background
# from flask import abort, flash, redirect, render_template, request, url_for
# from flask_login import current_user, login_required, login_user, logout_user
# from PIL import Image
# from flaskblog import app, db, bcrypt, mail
# from flaskblog.forms import (
#     LoginForm,
#     PostForm,
#     RegistrationForm,
#     UpdateAccountForm,
#     RequestResetForm,
#     ResetPasswordForm,s
# )
# from flaskblog.models import Post, User
# from flask_mail import Message


# from flask import current_app
# from flaskblog.database import db_check, db_initialize


# # https://flask.palletsprojects.com/en/1.1.x/cli/
# # import click
# # @click.command('initdb')
# @current_app.cli.command("initdb")
# def initialize_db():
#     """ Reinitialize the database and preload """
#     db_initialize()
#     return


# # import click
# # @click.command('check')
# @current_app.cli.command("check")
# def check_db():
#     db_check()
#     return
