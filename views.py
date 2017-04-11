from main import app
from flask import render_template, request, redirect, url_for, session, flash
from actions import login, logout, register_user, content_functions, get_post_by_title, get_comments_by_post, \
    post_comment;
from settings import get_name, fetch_settings
from functools import wraps
import json


# resize image  -- https://pypi.python.org/pypi/python-resize-image

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': get_name()['value']}
    return render_template('home/index.html', user=user)


@app.route('/about')
def about():
    contents =fetch_settings()
    print(contents)
    user = {'nickname': contents['name']}
    about = {'content': contents['about']}
    return render_template('home/about.html', user=user, about=about)


@app.route('/contact')
def contact():
    user = {'nickname': get_name()['value']}
    return render_template('home/contact.html', user=user)


count = 0


@app.route('/<title>')
def post(title):
    user = {'nickname': get_name()['value']}
    global count
    count += 1
    print(count)
    if title == "":
        return
    # fetch the other details from the database
    try:
        post = get_post_by_title(title)
    except:
        # change to 404 not found
        post = ""
        return redirect(url_for('error'))
    return render_template('home/post.html', user=user, post=post)


@app.route('/load_comments', methods=['POST'])
def load_comments():
    postid = request.json['id']
    print(postid)
    comments = get_comments_by_post(postid)
    return json.dumps(comments)


@app.route('/make_comment', methods=['POST'])
def make_comment():
    name = request.json['name']
    email = request.json['email']
    comment = request.json['comment']
    postid = request.json['postid']
    print("POSTING")
    try:
        post_comment(name, email, comment, postid)
        return "SUCCESS"
    except:
        return redirect(url_for('error'))
    return "FAIL"

@app.route('/error')
def error():
    user = {'nickname': get_name()['value']}
    return render_template('home/error.html', user=user)