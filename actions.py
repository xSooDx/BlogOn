import MySQLdb
from MySQLdb import escape_string as thwart
from flask import session
from passlib.hash import sha256_crypt
from BlogOnDB import *
import gc

from blogon_events import logEvent


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


def get_categories():
    c, conn = connect()
    c.execute('SELECT name FROM categories ')
    categories = c.fetchall()
    return categories


def get_child_categories(category):
    c, conn = connect()
    c.execute('SELECT * FROM categories WHERE parent=%s', (thwart(category),))
    categories = c.fetchall()
    return categories


def get_top_level_categories():
    c, conn = connect()
    c.execute('SELECT * FROM categories WHERE parent=NULL')
    categories = c.fetchall()
    return categories


def get(type, **clause):
    pass


# COMMENTS
def get_comments_by_post(postid):
    c, conn = connect()
    c.execute("SELECT name,comment FROM comments WHERE postid=%s", (int(postid),))
    data = c.fetchall()
    comments = []
    for comm in data:
        comments.append({'name': comm['name'], 'com': comm['comment']})
    # comments = [i['category'] for i in cats]
    return {"comments": comments}


def post_comment(name, email, comment, postid):
    c, conn = connect()
    c.execute("INSERT INTO comments (postid, name,email,comment) values (%s,%s,%s,%s)", (postid, name, email, comment))
    conn.commit()
    close(c, conn)


def get_comments_by_email(email):
    pass


def get_comments_by_name(name):
    pass


def get_comment_by_id(id):
    pass


# USERS
def get_users():
    c, conn = connect()
    c.execute("SELECT userid,username,email,rank FROM post_category")
    d = c.fetchall()
    users = []
    for u in d:
        users.append(User(u['userid'], u['username'], u['email'], u['rank']))
    close(c, conn)
    return users


def get_user_by_id(userid):
    c, conn = connect()
    c.execute("SELECT userid,username,email,rank FROM users WHERE userid=%s", (int(userid),))
    d = c.fetchone()
    close(c, conn)
    return d


def get_post_categories(postid):
    c, conn = connect()
    c.execute("SELECT category FROM post_category WHERE postid=%s", (int(postid),))
    cats = c.fetchall()
    cats = [i['category'] for i in cats]
    close(c, conn)
    return cats


# POSTS
def get_num_posts():
    c, conn = connect()
    c.execute("SELECT count(*) as n FROM posts")
    a = c.fetchone()['n']
    close(c, conn)
    return a


def get_posts():
    c, conn = connect()
    c.execute("SELECT * FROM posts ORDER BY creation_date DESC ")
    data = c.fetchall()

    for post in data:
        c.execute("SELECT category FROM post_category WHERE postid=%s ", (int(post['postid']),))
        cats = get_post_categories(post['postid'])
        post['categories'] = cats
    close(c, conn)
    return data


def get_post_by_id(postid):
    c, conn = connect()
    c.execute("SELECT * FROM posts WHERE postid=%s ORDER BY creation_date", (int(postid),))
    data = c.fetchone()
    c.execute("SELECT category FROM post_category WHERE postid=%s", (int(postid),))
    cats = get_post_categories(postid)
    close(c, conn)
    data['categories'] = cats

    return data


def get_post_by_title(title):
    tstr = " ".join(title.split("-"))
    c, conn = connect()
    c.execute("SELECT * FROM posts WHERE title=%s", (tstr,))
    data = c.fetchone()
    c.execute("SELECT category FROM post_category WHERE postid=%s", (int(data['postid']),))
    cats = get_post_categories(data['postid'])
    close(c, conn)
    data['categories'] = cats
    return data


def get_posts_by_category(category):
    posts = []
    c, conn = connect()
    c.execute("SELECT postid FROM post_category where category=%s creation_date", (thwart(category),))
    data = c.fetchall()
    data = [i['postid'] for i in data]
    for i in data:
        c.execute("SELECT * FROM posts WHERE postid=%s", (int(i),))
        post = c.fetchone()
        cats = get_post_categories(i)
        post['categories'] = cats
        posts.append(post)
    close(c, conn)
    return posts


def get_posts_by_user(user):  # name or authorid
    c, conn = connect()

    if isinstance(user, str):
        c.execute("SELECT * FROM posts WHERE username=%s date_created", (thwart(user),))
        data = c.fetchall()
        for i in data:
            i['categories'] = get_post_categories(i['postid'])

    elif isinstance(user, int):
        c.execute("SELECT * FROM posts WHERE userid=%s", (int(user),))
        data = c.fetchall()
        for i in data:
            i['categories'] = get_post_categories(i['postid'])
    else:
        return -1
    close(c, conn)
    return data


def content_functions():
    funcs = {

        'get_num_posts': get_num_posts,
        'get_posts': get_posts,
        'get_posts_by_user': get_posts_by_user,
        'get_posts_by_id': get_post_by_id,
        'get_posts_by_category': get_posts_by_category,
        'get_categories': get_categories,
        'get_comments_by_post': get_comments_by_post,
        'get_comment_by_id': get_comment_by_id,
        'get_comments_by_name': get_comments_by_name,
        'get_comments_by_email': get_comments_by_email,
        'get_users': get_users,
        'get_user_by_id': get_user_by_id
    }
    return funcs


def create_post(**d):
    a = 0
    x = {
        'title': '',
        'content': '',
        'description': '',
        'categories': ['.'],
        'tags': ''
    }
    x.update(d)
    for i in x:
        if not (x[i] == "" or x[i] is None or x[i] == ['.'] or x[i] == []):
            a = 1
            break
    if a == 0:
        return -1
    c, conn = connect()

    c.execute("INSERT INTO posts (userid,title,content,description,tags) values (%s,%s,%s,%s,%s)",
              (int(session['userid']), thwart(x['title']), thwart(x['content']), thwart(x['description']),
               thwart(x['tags'])))

    c.execute("SELECT LAST_INSERT_ID() as id")
    postid = c.fetchone()['id']

    if 'categories' in x:

        for cat in x['categories']:
            c.execute("INSERT INTO post_category values(%s,%s)", (int(postid), thwart(cat)))

    conn.commit()
    close(c, conn)
    logEvent("post create", "userid=" + str(session['userid']) + " postid=" + str(postid))
    return postid


def update_post(postid, **d):
    c, conn = connect()
    x = {
        'title': '',
        'content': '',
        'description': '',
        'categories': [],
        'tags': ''
    }
    x.update(d)
    a = 0
    qstr = ""
    data = []
    for i in x:
        if not (x[i] == "" or x[i] is None or x[i] == []):
            a = 1
            if i in ('title', 'description', 'content', 'tags', 'published'):
                qstr += (i + "=%s,")
                data.append(thwart(x[i]))
    if a == 0:
        return -1
    data.append(int(session['userid']))
    data.append(int(postid))
    c.execute("UPDATE posts SET " + qstr + " modified_date=CURRENT_TIMESTAMP WHERE userid= %s AND postid=%s", data)

    c.execute("SELECT category FROM post_category WHERE postid=%s", (int(postid),))
    cats = c.fetchall()
    cats = set([i['category'] for i in cats])
    if 'categories' in x:
        cats2 = set(x['categories'])
        rm = cats - cats2
        for i in rm:
            c.execute("DELETE FROM post_category WHERE postid=%s and category=%s", (int(postid), i))
        ad = cats2 - cats
        for i in ad:
            c.execute("INSERT INTO post_category values(%s, %s)", (int(postid), i))

    conn.commit()
    close(c, conn)
    logEvent("post update", "userid=" + str(session['userid']) + " postid=" + str(postid))
    return postid


def publish_post(postid):
    c, conn = connect()
    c.execute("UPDATE posts SET published=1 WHERE postid=%s and userid=%s", (int(postid), int(session['userid'])))
    conn.commit()
    close(c, conn)
    logEvent("post publish", "userid=" + str(session['userid']) + " postid=" + str(postid))
    return postid


def unpublish_post(postid):
    c, conn = connect()
    c.execute("UPDATE posts SET published=0 WHERE postid=%s and userid=%s", (int(postid), int(session['userid'])))
    conn.commit()
    close(c, conn)
    logEvent("post unpublish", "userid=" + str(session['userid']) + " postid=" + str(postid))
    return postid


def delete_post(postid):
    c, conn = connect()
    c.execute("DELETE FROM posts WHERE userid=%s AND postid=%s", (int(session['userid']), int(postid)))
    conn.commit()
    close(c, conn)
    logEvent("post delete", "userid=" + str(session['userid']) + " postid=" + str(postid))
    return postid


def login(username, password, remember=False):
    c, conn = connect()
    res = c.execute("SELECT * FROM users WHERE (username=%s OR email=%s) AND NOT rank=-1",
                    (thwart(username), thwart(username)))
    ret = 0

    if res > 0:
        print('a')
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
    logEvent("user register", "userid=" + userid)
    return userid


def set_login_session(userid, username, email):
    session['logged_in'] = True
    session['userid'] = userid
    session['username'] = username
    session['email'] = email
    return User(userid, username, email)


def logout():
    session.clear()
