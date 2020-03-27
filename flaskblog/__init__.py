# initialize application and bring in various components

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# python -> import secrets -> secrets.token_hex(16)
app.config["SECRET_KEY"] = "57383f18a431c57cc60880218eff93c6"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = "False"
# database_file = '"sqlite://flaskblog/preload.db"'  # site
# sqlite:/// is a relative path
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/site.db"

# Valid SQLite URL forms are:
# sqlite:///:memory: (or, sqlite://)
# sqlite:///relative/path/to/file.db
# sqlite:////absolute/path/to/file.db
# Invalid SQLite URL: sqlite://../C:\dev\src\Python\FlaskBlog\flaskblog\db/site.db
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://../db/site.db"
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"  # the function, like url_for
login_manager.login_message_category = "info"

# cannot import at the top (circular import) -- needs app, db, bcrypt
from flaskblog import routes
