import json
import os
from datetime import datetime

from flask import current_app, flash, redirect, render_template, url_for
from sqlalchemy import text

from flaskblog import app, bcrypt, db
from flaskblog.models import Post, User

_SQL_COUNT = "select count(*) from {table}"


def _get_count(table):
    sql = _SQL_COUNT.format(table=table)
    result = _execute_sql(sql)
    row = result.first()
    return row[0]


def _execute_sql(sql_statement):
    output = "ok"
    try:
        # from sqlalchemy import text
        # result = session.execute(text("SELECT * FROM user WHERE id=:param"), {"param":5})
        result = db.session.execute(sql_statement)
    except Exception as ex:
        output = str(ex)
        print(repr(ex))
    return result


def _check_status():
    is_database_working = True
    output = "ok"

    try:
        # to check database we will execute raw query
        # session = db.current_app.get_database_session()
        # query will create the db file if doesn't exist
        db.session.query("1").from_statement(text("SELECT 1")).all()
        # db.session.execute("SELECT 1")
        # db.engine.execute(text("SELECT 1"))
    except Exception as ex:
        output = str(ex)
        is_database_working = False
        print(repr(ex))

    return is_database_working, output


def db_initialize():
    """ Initialize database and pre-load with data. """
    db_up, db_status = _check_status()
    if db_up == False:
        print("Failed DB check, aborting DB initialize.")
        return

    print("Creating schema...")
    try:
        # drop all may error if tables don't exist, eat it and assume create will work
        db.drop_all()
    except Exception as ex:
        print(repr(ex))
    db.create_all()

    # try:
    #     # just see if we can load and read the db schema for use of concept elsewhere
    #     with current_app.open_resource("db/schema.sql") as f:
    #         print(f.read().decode("utf8"))
    #         # db.executescript(f.read().decode("utf8"))
    # except Exception as ex:
    #     print(repr(ex))

    # flash("Post deleted.", "success")
    print("Populating schema...")
    # load json data file
    with current_app.open_resource("db/preload.json") as preload_file:
        # print(f.read().decode("utf8"))
        data = json.load(preload_file)

    # app.root_path --> root of app
    # app.static_folder --> {app root}\static
    # filename = os.path.join(app.root_path, "db\\preload.json")
    # with open(filename) as preload_file:
    #     data = json.load(preload_file)

    # populate users
    for user_data in data["users"]:
        hashed_password = bcrypt.generate_password_hash(user_data["password"]).decode(
            "utf-8"
        )
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            password=hashed_password,
        )
        db.session.add(user)
    db.session.commit()
    print("{} users added.".format(_get_count("user")))

    # populate posts
    for post_data in data["posts"]:
        user_id = int(post_data["user_id"])
        # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        # datetime_obj = datetime.strptime(post_data["posted"], "%b %d %Y %I:%M%p")
        datetime_obj = datetime.strptime(post_data["posted"], "%b %d %Y %H:%M:%S")
        post = Post(
            title=post_data["title"],
            content=post_data["content"],
            user_id=user_id,
            posted=datetime_obj,
        )
        db.session.add(post)
    db.session.commit()
    print("{} posts added.".format(_get_count("post")))


def db_check():
    """ Check the health status of the database """
    engine = db.get_engine()
    url = engine.url
    print("----- Database Information")
    # print("url:    ", url)
    print("db:     ", url.database)
    print("driver: ", url.drivername)
    print("host:   ", url.host)
    print("port:   ", url.port)
    db_up, db_status = _check_status()
    print("status: ", db_status)
