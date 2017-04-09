from flask import flash, jsonify
from flask import request, redirect
from flask import url_for

from main import app
from blogon_views import blogon_login_required
from actions import create_post, update_post, publish_post, delete_post


@app.route("/blogon/tasks/post/create", methods=['POST'])
@blogon_login_required
def create_post_task():
    l = request.values.getlist('categories')
    l.pop(0)
    a = create_post(title=request.values['title'],
                    content=request.values['content'],
                    description=request.values['description'],
                    categories=l,
                    tags=request.values['tags'])

    flash("Post Saved")
    return jsonify(result=a)


@app.route("/blogon/tasks/post/update", methods=['POST'])
@blogon_login_required
def update_post_task():
    l = request.values.getlist('categories')
    l.pop(0)
    a = update_post(request.values['postid'],
                    title=request.values['title'],
                    content=request.values['content'],
                    decription=request.values['description'],
                    categories=l,
                    tags=request.values['tags'])
    return jsonify(result=a)


@app.route("/blogon/tasks/post/publish", methods=['POST'])
@blogon_login_required
def publish_post_task():
    a = publish_post(request.form['postid'])
    flash("Your post has been published.")
    return redirect(url_for('posts_page'))


@app.route("/blogon/tasks/post/delete", methods=['POST'])
@blogon_login_required
def delete_post_task():
    a = delete_post(request.values['postid'])
    if a == -1:
        flash("You are not the author of this post")
    else:
        flash("Post has been deleted")
    return redirect(url_for('posts_page'))
