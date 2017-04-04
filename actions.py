import MySQLdb
from MySQLdb import escape_string as thwart
from flask import session
from passlib.hash import sha256_crypt
from BlogOnDB import *
import gc


def close(c, conn):
    c.close()
    conn.close()
    gc.collect()


def connect():
    conn = MySQLdb.connect(
        host="localhost",
        user="blogon_user",
        passwd="blogon",
        db="blogon_db",
    )
    c = conn.cursor(MySQLdb.cursors.DictCursor)

    return c, conn


def get(type, **clause):
    pass


# COMMENTS
def get_comments_by_post(postid):
    c, conn = connect();


def get_comments_by_email(email):
    pass


def get_comments_by_name(name):
    pass


def get_comment_by_id(id):
    pass


# POSTS
def get_post_by_id(id):
    pass


def get_posts_by_category(category):
    pass


def get_posts_by_author(author):  # name or authorid
    if isinstance(author, str):
        pass
    elif isinstance(author, int):
        pass


def create_post(**x):
    pass


def update_post():
    pass


def login(username, password, remember=False):
    c, conn = connect()
    res = c.execute("SELECT * FROM users WHERE (username=%s OR email=%s) AND NOT rank=-1",
                    (thwart(username), thwart(username)))
    ret = 0
    if res > 0:
        row = c.fetchone()
        if sha256_crypt.verify(password, row['passwordhash']):
            # login successful, set session vars.
            set_login_session(row['userid'], row['username'], row['email'])
            c.execute("UPDATE users SET last_login=CURRENT_TIMESTAMP")
            conn.commit()
            ret = 1
    close(c, conn)
    return ret


def register_user(username, email, password):
    c, conn = connect()
    tusername, temail = thwart(username), thwart(email)
    n = c.execute("SELECT * FROM users WHERE username=%s OR email=%s", (tusername, temail))
    if n > 0:
        return 0
    password = sha256_crypt.encrypt(password)
    c.execute("INSERT INTO users (username,email,passwordhash) values (%s,%s,%s)",
              (tusername, temail, thwart(password)))
    conn.commit()
    c.execute("SELECT userid FROM users WHERE username=%s", (tusername,))
    userid = c.fetchone()['userid']
    set_login_session(userid, username, email)
    close(c, conn)
    return 1


def set_login_session(userid, username, email):
    session['logged_in'] = True
    session['userid'] = userid
    session['username'] = username
    session['email'] = email
    return User(userid, username, email)


def logout():
    session.clear()
