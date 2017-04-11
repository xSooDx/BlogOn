import os

from flask import flash, jsonify, Response
from flask import request, redirect
from flask import url_for
from time import sleep

from werkzeug.utils import secure_filename

from blogon_events import checkLogTime, logTail
from main import app
from blogon_views import blogon_login_required
from actions import create_post, update_post, publish_post, delete_post, unpublish_post


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
    return jsonify(result=a)


@app.route("/blogon/tasks/post/unpublish", methods=['POST'])
@blogon_login_required
def unpublish_post_task():
    a = unpublish_post(request.form['postid'])
    flash("Your post has been unpublished.")
    return jsonify(result=a)


@app.route("/blogon/tasks/post/delete", methods=['POST'])
@blogon_login_required
def delete_post_task():
    a = delete_post(request.values['postid'])
    if a == -1:
        flash("You are not the author of this post")
    else:
        flash("Post has been deleted")
    return redirect(url_for('posts_page'))


@app.route("/blogon/task/logstream")
@blogon_login_required
def log_stream():
    def log():
        oldLog = 0
        for i in range(10):
            newLog = checkLogTime()
            if newLog > oldLog:
                oldLog = newLog
                data = logTail()
                res = "event: logUpdate\n"
                res += "retry: 2000\n"
                res += "data: { 'logs' :" + str(data) + "}\n\n"
                yield res.encode()
            sleep(2)

    return Response(log(), mimetype="text/event-stream")


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/blogon/task/upload_img",methods=['POST'])
@blogon_login_required
def upload_img_task():
    path = ""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
    return jsonify({"location": url_for('static',filename=("uploads/"+filename))})
