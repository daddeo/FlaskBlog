import os
import json
import sqlite3
from sqlite3 import Error
from datetime import datetime
from flask import current_app

# from flask_bcrypt import Bcrypt

# from flaskblog import db
# from flaskblog.models import User, Post

# https://likegeeks.com/python-sqlite3-tutorial/
# https://www.sqlitetutorial.net/sqlite-python/
# https://www.sqlitetutorial.net/sqlite-commands/


json_data_file = "db/preload.json"
# r"C:\sqlite\db\pythonsqlite.db"
database_file = '"sqlite://flaskblog/preload.db"'  # site
sql_user_table_drop = """
    drop table if exists user;
    """
sql_user_table_create = """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER NOT NULL, 
        username VARCHAR(20) NOT NULL, 
        email VARCHAR(120) NOT NULL, 
        password VARCHAR(60) NOT NULL, 
        image_file VARCHAR(20) NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (username), 
        UNIQUE (email)
    );
    """
sql_user_table_insert = """
    INSERT INTO user (username, email, password) VALUES (?, ?, ?);
    """
sql_post_table_drop = """
    drop table if exists post;
    """
sql_post_table_create = """
    CREATE TABLE IF NOT EXISTS post (
        id INTEGER NOT NULL, 
        title VARCHAR(100) NOT NULL, 
        content TEXT NOT NULL, 
        posted DATETIME NOT NULL, 
        modified DATETIME NULL, 
        user_id INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(user_id) REFERENCES user (id)
    );
    """
sql_post_table_insert = """
    INSERT INTO post (title, content, posted, modified, user_id) VALUES (?, ?, ?, ?, ?);
    """


def db_create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("connected to sqlite ", sqlite3.version)
    except Error as e:
        print(e)
    finally:
        pass
        # if conn:
        #     conn.close()

    return conn


def db_create_table(conn, sql_drop_table, sql_create_table):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param sql_drop_table: a DROP TABLE statement
    :param sql_create_table: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()

        c.execute(sql_drop_table)
        conn.commit()

        c.execute(sql_create_table)
        conn.commit()
    except Error as e:
        print(e)


def db_execute(conn, sql, substitutions):
    """ execute the provided sql statement
    :param conn: Connection object
    :param sql: the sql statement
    :return: the lastrowid
    """
    cursorObj = conn.cursor()
    if substitutions != None:
        cursorObj.execute(sql, substitutions)
    else:
        cursorObj.execute(sql)
    conn.commit()
    # cursorObj.close()
    return cursorObj.lastrowid


def json_load(file):
    basedir = os.path.dirname(__file__)
    # 'relative/path/to/file.json'
    file_path = os.path.join(basedir, db_connstr)
    with open(file_path, "r") as f:
        data = json.load(f)
    f.close()
    print("-------------------------------------------------")
    print("start json data")
    print("-------------------------------------------------")
    print(data)
    print("-------------------------------------------------")
    print("end json data")
    print("-------------------------------------------------")
    return data


def preload_db_data():

    print("app name: ", __name__)
    data = json_load(json_data_file)
    conn = db_create_connection(database_file)

    # create tables
    if conn is None:
        print("Error! cannot create the database connection.")
        return

    # create user table
    print("-------------------------------------------------")
    print("create user table")
    print("-------------------------------------------------")
    db_create_table(conn, sql_user_table_drop, sql_user_table_create)
    # conn.commit()

    # INSERT INTO user (username, email, password) VALUES (?, ?, ?);
    print("-------------------------------------------------")
    print("insert user data")
    print("-------------------------------------------------")
    for user_data in data["users"]:
        hashed_password = bcrypt.generate_password_hash(user_data["password"]).decode(
            "utf-8"
        )
        user = (user_data["username"], user_data["email"], hashed_password)
        db_execute(conn, sql_user_table_insert, user)
    # conn.commit()

    # create post table
    print("-------------------------------------------------")
    print("create post table")
    print("-------------------------------------------------")
    db_create_table(conn, sql_post_table_drop, sql_post_table_create)
    # conn.commit()

    # INSERT INTO post (title, content, posted, modified, user_id) VALUES (?, ?, ?, ?, ?);
    print("-------------------------------------------------")
    print("insert post data")
    print("-------------------------------------------------")
    for post_data in data["posts"]:
        post = (
            post_data["title"],
            post_data["content"],
            post_data["posted"],
            datetime.utcnow(),
            post_data["user_id"],
        )
        db_execute(conn, sql_post_table_insert, post)
    # conn.commit()

    conn.close()
