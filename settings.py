from main import app
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from actions import connect,close

@app.route('/update_name', methods=['POST'])
def update_name():
	name = request.json['name']
	about = request.json['about']
	c, conn = connect()	
	c.execute("SELECT * FROM settings WHERE setting='name'")
	val = c.fetchone();
	if(val==None):
		c.execute("INSERT INTO settings(setting, value) values(%s,%s)",('name',str(name)))
	else:
		c.execute("UPDATE settings SET value = %s WHERE setting = %s", (str(name), 'name'))
	c.execute("UPDATE settings SET value = %s WHERE setting = %s", (str(about), 'about'))
	#c.execute("IF EXISTS (SELECT * FROM settings WHERE setting='name') BEGIN UPDATE settings SET value = %s WHERE setting = 'name' END ELSE BEGIN INSERT INTO settings(setting, value) values('name',%s) END",(name,name))
	conn.commit()
	
	close(c, conn)
	return "SUCCESS"
	
def get_name():
	c, conn = connect()	
	c.execute("SELECT value FROM settings WHERE setting='name'")
	val = c.fetchone();
	print (val)
	close(c, conn)
	return val

	
@app.route("/get_settings", methods=['POST'])
def get_settings():
	values = fetch_settings()
	return jsonify(values)
	
def fetch_settings():
	c, conn = connect()	
	c.execute("SELECT value FROM settings WHERE setting='name'")
	val = c.fetchone();
	c.execute("SELECT value FROM settings WHERE setting='about'")
	val2 = c.fetchone();
	values = {'name':val['value'], 'about':val2['value']}
	close(c, conn)
	return values