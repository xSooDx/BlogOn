from main import app
from flask import render_template, request, redirect, url_for, session, flash
from actions import login, logout, register_user, content_functions, get_post_by_title ;
from functools import wraps

##resize image  -- https://pypi.python.org/pypi/python-resize-image

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'MIGUEL'}
	return render_template('home/index.html',user=user)
	
@app.route('/about')
def about():
	user = {'nickname': 'MIGUEL'}
	return render_template('home/about.html',user=user)
	
@app.route('/contact')
def contact():
	user = {'nickname': 'MIGUEL'}
	return render_template('home/contact.html',user=user)
	
count=0
@app.route('/<title>')
def post(title):
	global count
	count+=1
	print(count)
	if(title==""):
		return
	#fetch the other details from the database 
	user = {'nickname': 'MIGUEL'}
	try:
		post = get_post_by_title(title)
	except:
		#change to 404 not found
		render_template("home/index.html")
	return render_template('home/post.html',user=user,n_comm= 2, post=post)
	