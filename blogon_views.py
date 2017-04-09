from main import app
from flask import render_template, request, redirect, url_for, session, flash
from actions import login, logout, register_user, content_functions;
from functools import wraps


class PageData:
    def __init__(self, name, title, description=""):
        self.name = name
        self.title = title
        self.description = description


def blogon_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You are not logged in.")
            return redirect(url_for('login_page'))

    return wrap




@app.route("/blogon/", methods=['GET'])
@app.route("/blogon/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if login(username, password):
            return redirect(url_for("dashboard_page"))
        else:
            flash("Invalid login credentials")
            return redirect(url_for("login_page"))
    else:
        if 'logged_in' in session:
            flash("You are already logged in")
            return redirect(url_for("dashboard_page"))
        page = PageData("login", "Login", "Register your details")
        return render_template("BlogOn/login.html", page=page)


# not everyone should be able to register to a blog need to revise this
@app.route("/blogon/register", methods=["GET", "POST"])
def register_page():
    try:
        if request.method == "POST":
            password = request.form['password']
            confirm = request.form['confirm']
            username = request.form['username']
            email = request.form['email']
            if not password == confirm:
                return render_template("BlogOn/register.html", message="Passwords do not match")
            if not register_user(username, email, password):
                return render_template("BlogOn/register.html", message="Username or email already taken")
            else:
                return redirect(url_for("dashboard_page"))
        else:
            page = PageData("register", "Register", "Register your details")
            return render_template("BlogOn/register.html", page=page)

    except Exception as e:
        return "oops: " + str(e)


@app.route("/blogon/dashboard")
@blogon_login_required
def dashboard_page():
    page = PageData("dashboard", "Dashboard", "Site Dashboard")
    return render_template("BlogOn/dashboard.html", page=page)


@app.route("/blogon/settings")
@blogon_login_required
def settings_page():
    page = PageData("settings", "Settings", "Manage site settings")
    return render_template("BlogOn/pages.html", page=page)


@app.route("/blogon/pages")
@blogon_login_required
def pages_page():
    page = PageData("pages", "Pages", "View and manage all your pages")
    return render_template("BlogOn/pages.html", page=page)


@app.route("/blogon/posts")
@blogon_login_required
def posts_page():
    page = PageData("posts", "Posts", "View and manage all your posts")
    return render_template("BlogOn/posts.html", page=page)


@app.route("/blogon/create_post")
@blogon_login_required
def create_post_page():
    page = PageData("create_post", "Create Post")
    return render_template("BlogOn/create_post.html", page=page)


@app.route("/blogon/profile")
@blogon_login_required
def profile_page():
    page = PageData("profile", session["username"] + "'s profile", "Manage your profile settings")
    return render_template("BlogOn/profile.html", page=page)


@app.route("/blogon/logout")
@blogon_login_required
def logout_page():
    logout()
    return redirect(url_for('root'))


@app.context_processor
def content_processor():
    return content_functions()
