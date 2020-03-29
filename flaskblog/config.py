import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # python -> import secrets -> secrets.token_hex(16)
    SECRET_KEY = os.environ.get("FLASKBLOG_SECRET_KEY")

    SQLALCHEMY_TRACK_MODIFICATIONS = "False"

    # Valid SQLite URL forms are:
    # sqlite:///:memory: (or, sqlite://)
    # sqlite:///relative/path/to/file.db
    # sqlite:////absolute/path/to/file.db
    # Invalid SQLite URL: sqlite://../C:\dev\src\Python\FlaskBlog\flaskblog\db/site.db
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://../db/site.db"

    # datbase_file = '"sqlite://flaskblog/preload.db"'  # site
    # sqlite:/// is a relative path
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    SQLALCHEMY_DATABASE_URI = os.environ.get("FLASKBLOG_SQLALCHEMY_DATABASE_URI")

    # "smtp.googlemail.com"
    MAIL_SERVER = os.environ.get("FLASKBLOG_MAIL_SERVER", "smtp.comcast.net")
    MAIL_PORT = int(os.environ.get("FLASKBLOG_MAIL_PORT", "587"))
    MAIL_USE_TLS = os.environ.get("FLASKBLOG_MAIL_TLS", "true").lower() in [
        "true",
        "on",
        "1",
    ]
    MAIL_USERNAME = os.environ.get("FLASKBLOG_MAIL_USER")
    MAIL_PASSWORD = os.environ.get("FLASKBLOG_MAIL_PASSWORD")

    FLASKBLOG_MAIL_SUBJECT_PREFIX = "[FlaskBlog]"
    FLASKBLOG_MAIL_SENDER = "FlaskBlog Admin <flagblog@example.com>"
    FLASKBLOG_ADMIN = os.environ.get("FLASKBLOG_ADMIN", "")

    # @staticmethod
    # def init_app(app):
    #     pass
