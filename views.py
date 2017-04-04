from main import app
from flask import render_template, request, redirect, url_for, session
from actions import login, logout, register_user
from functools import wraps


def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            return redirect(url_for('login)page'))
    return wrap


@app.route('/')
def root():
    return "<a href='/login'>Login</a>"


@app.route("/blogon/login", methods=["GET", "POST"])
def login_page():
    # try:
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if login(username, password):
            return redirect(url_for("dashboard_page"))
        else:
            return redirect(url_for("login_page"))
    else:
        return render_template("BlogOn/login.html")
    # except Exception as e:
    return "oops " + str(e)


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
            return render_template("BlogOn/register.html")

    except Exception as e:
        return "oops: " + str(e)


@app.route("/blogon/dashboard")
@login_required
def dashboard_page():
    return render_template("BlogOn/dashboard.html")


@app.route("/blogon/logout")
@login_required
def logout_page():
    logout()
    return redirect(url_for('root'))
