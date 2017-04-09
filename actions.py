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
    c.execute('SELECT * FROM categories WHERE parent=NULL');
    categories = c.fetchall()
    return categories


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


# USERS
def get_users():
    pass


def get_users_by_id():
    pass


def get_post_categories(postid):
    c, conn = connect()
    c.execute("SELECT category FROM post_category WHERE postid=%s", (int(postid),))
    cats = c.fetchall()
    cats = [i['category'] for i in cats]
    return cats


# POSTS
def get_num_posts():
    c, conn = connect()
    c.execute("SELECT count(*) as n FROM posts")
    return c.fetchone()['n']


def get_posts():
    c, conn = connect()
    c.execute("SELECT * FROM posts")
    data = c.fetchall()
    posts = []
    for post in data:
        c.execute("SELECT category FROM post_category WHERE postid=%s", (int(post['postid']),))
        cats = get_post_categories(post['postid'])
        posts.append(Post(post['postid'], post['userid'], post['title'], post['content'], post['description'], cats,
                          post['tags']))
    close(c, conn)
    return posts


def get_post_by_id(postid):
    c, conn = connect()
    c.execute("SELECT * FROM posts WHERE postid=%s", (int(postid),))
    data = c.fetchone()
    c.execute("SELECT category FROM post_category WHERE postid=%s", (int(postid),))
    cats = get_post_categories(postid)
    close(c, conn)
    return Post(data['postid'], data['userid'], data['title'],
                data['content'], data['description'], data['tags'], cats)

def get_post_by_title(title):
    str = " ".join(title.split("-"))
    c, conn = connect()
    c.execute("SELECT * FROM posts WHERE title=%s", (str,))
    data = c.fetchone()
    c.execute("SELECT category FROM post_category WHERE postid=%s", (int(data['postid']),))
    cats = get_post_categories(data['postid'])
    close(c, conn)
    return Post(data['postid'], data['userid'], data['title'],
                data['content'], data['description'], data['tags'], cats)

def get_posts_by_category(category):
    posts = []
    c, conn = connect()
    c.execute("SELECT postid FROM post_category where category=%s", (thwart(category),))
    data = c.fetchall()
    data = [i['postid'] for i in data]
    for i in data:
        c.execute("SELECT * FROM posts WHERE postid=%s", (int(i),))
        post = c.fetchone()
        cats = get_post_categories(i)
        posts.append(Post(post['postid'], post['userid'], post['title'], post['content'], post['description'], cats,
                          post['tags']))
    close(c, conn)
    return posts


def get_posts_by_user(user):  # name or authorid
    c, conn = connect()
    posts = []
    if isinstance(user, str):
        c.execute("SELECT * FROM posts WHERE username=%s", (thwart(user),))
        data = c.fetchall()
        for i in data:
            posts.append(Post(i['postid'], i['userid'], i['title'], i['content'], i['description'],
                              get_post_categories(i['postid']), i['tags']))

    elif isinstance(user, int):
        c.execute("SELECT * FROM posts WHERE userid=%s", (int(user),))
        data = c.fetchall()
        for i in data:
            posts.append(Post(i['postid'], i['userid'], i['title'], i['content'], i['description'],
                              get_post_categories(i['postid']), i['tags']))
    return posts

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
        'get_users_by_id': get_users_by_id
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
        print(cats)
        print(cats2)
        print(rm)
        for i in rm:
            c.execute("DELETE FROM post_category WHERE postid=%s and category=%s", (int(postid), i))
        ad = cats2 - cats
        print(ad)
        for i in ad:
            c.execute("INSERT INTO post_category values(%s, %s)", (int(postid), i))

    conn.commit()
    close(c, conn)


def publish_post(postid):
    c, conn = connect()
    c.execute("UPDATE posts SET published=1 WHERE postid=%s", (int(postid),))
    conn.commit()
    close(c, conn)


def delete_post(postid):
    c, conn = connect()
    c.execute("DELETE FROM posts WHERE userid=%s AND postid=%s", (int(session['userid']), int(postid)))
    conn.commit()
    close(c, conn)


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
    return 1


def set_login_session(userid, username, email):
    session['logged_in'] = True
    session['userid'] = userid
    session['username'] = username
    session['email'] = email
    return User(userid, username, email)


def logout():
    session.clear()
