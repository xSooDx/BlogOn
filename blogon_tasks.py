from flask import flash, jsonify
from flask import request
from main import app
from blogon_views import blogon_login_required
from actions import create_post, update_post, publish_post


@app.route("/blogon/tasks/post/create", methods=['POST'])
@blogon_login_required
def create_post_task():
    l = request.values.getlist('categories')
    l.pop[0]
    a = create_post(title=request.values['title'],
                    content=request.values['content'],
                    description=request.values['description'],
                    categories=request.values.getlist('categories'),
                    tags=request.values['tags'])

    return jsonify(result=a)


@app.route("/blogon/tasks/post/update", methods=['POST'])
@blogon_login_required
def update_post_task():
    l = request.values.getlist('categories')
    l.pop[0]
    a = update_post(title=request.values['title'],
                    content=request.values['content'],
                    decription=request.values['description'],
                    categories=l,
                    tags=request.values['tags'])
    return jsonify(result=a)


@app.route("/blogon/tasks/post/publish", methods=['POST'])
@blogon_login_required
def publish_post_task():
    publish_post(request.form['postid'])
    flash("Your post has been published.")
