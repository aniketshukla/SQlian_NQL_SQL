from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash
#import redis

login=Flask(__name__)
#alternative to config.py
DEBUG=True
SECRET_KEY='development key'
USERNAME='admin'
PASSWORD='default'
#config over
login.config.from_object(__name__)

@login.route('/',methods=["GET","POST"])
def load_page():
	return render_template("init.html")
@login.route('/register/',methods=["GET","POST"])
def register():
	render=request.form()
	return render[0]


login.run()

