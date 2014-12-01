from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash,redirect
import redis
import time
from flask.ext.login import LoginManager
from functools import wraps
import psycopg2
import sys
import execute
import languageprocess1.sqlizer
import languageprocess1.tokenizer
import sys
import os
from datetime import datetime
usernametemp="default"
login=Flask(__name__)
#alternative to config.py
DEBUG=True
SECRET_KEY='development key'
USERNAME='admin'
PASSWORD='default'
SECRET_KEY="hashmein"
#config over
login.config.from_object(__name__)
login_manager=LoginManager()
login_manager.init_app(login)



def redis_connect():
	return redis.Redis("localhost")

@login.route('/')
def load_page():
	return render_template("init.html")
@login.route('/register',methods=['GET','POST'])
def register():
	name=request.form["name"]
	email=request.form["email"]
	date=request.form["date"]
	password=request.form["password"]
	render=redis_connect()
	temp=render.hget(email,"email")
	error=""
	if temp==None:
		render.hset(email,"name",name)
		render.hset(email,"email",email)
		render.hset(email,"date",date)
		render.hset(email,"password",password)
		temp="your account has been set...happy surfing "
	else:
		temp="email id already exists....try with a different id"
	flash(temp)
	try:
		em=list(email)
		em.remove("@")
		em.remove(".")
		em="".join(em)
		con=psycopg2.connect(database='blog_log',user='postgres',password='ssww33')
		cur=con.cursor()
		copy='''CREATE TABLE '''+em+''' (date TIMESTAMP PRIMARY KEY ,blog text ,likes int ,comments text );'''
		cur.execute(copy)
		con.commit()
	except:
		temp="oopsie looks like our hamsters got tired already...try again"
		render.delete(email)
	return render_template("roll.html",temp=temp)


@login.route('/dashin',methods=['GET','POST'])
def dashn():
	render=redis_connect()
	email=request.form["email"]
	password=request.form["password"]
	temp=render.hget(email,"email")
	xamp=password
	xamp=bytes(xamp,"UTF-8")
	if temp==None :
		error="your email id does not exist...try again or create a new account"
		return render_template("roll.html",temp=error)
	else:
		error=""
	if xamp!=render.hget(email,"password"):
		error="wrong password"
		return render_template("roll.html",temp=error)
	else:
		error=""
	session["email"]=render.hget(email,"email")
	####dashboard execution begins
	username=render.hget(email,"name")
	global usernametemp
	g.usernametemp=username
	#xamp=bytes(username,"UTF-8")
	return redirect(b"/user/"+username)

@login.route('/user/<string:username>')
def dashboard(username):
	#forms the required dashboard action in the future
	return render_template("dashboardpopleft.html",username=username)

@login.route('/user/<string:username>/editor')
def editor(username):
        a=session["email"]
        return render_template("editor.html",username=username)

@login.route('/user/<string:username>/render',methods=['GET','POST'])
def render(username):
    a=session["email"]
    a=str(a)
    a=list(a)
    p=a[2:len(a)-1]
    a=p
    i=datetime.now()
    i=str(i)
    header=request.form["header"]
    entry=request.form["entry"]
    completeblog='''<div class="panel panel-default"><div class="panel-heading">'''+header+'''</div><!-- /.panel-heading --><div class="panel-body">'''+entry+'''</div><!-- /.panel-body --></div>'''
    em=list(a)
    em.remove("@")
    em.remove(".")
    em="".join(em)
    con=psycopg2.connect(database='blog_log',user='postgres',password='ssww33')
    cur=con.cursor()
    query='''INSERT INTO '''+em+'''(date  ,blog  ,likes  ,comments)VALUES(CURRENT_TIMESTAMP,'''+completeblog+''',0,0)'''
    cur.execute(query)
    con.commit()
    return redirect(url_for("editor"))

@login.route('/user/<string:username>/masterquery')
def masterquery(username):
    return render_template("querymaster.html",username=username)

@login.route('/user/<string:username>/schemagenerator')        
def generate(username):
	return render_template("schemag.html",username=username)

@login.route('/user/<string:username>/result',methods=["GET","POST"])
def result(username):
    query = request.form['query']
    squery = languageprocess1.sqlizer.sqlize(query)
    s = execute.execi(squery)
    global quer 
    quer = squery
    print(quer)
    if not s:
        result = "Executed Successfully:" + quer
        session['result'] = result
        return str(result)
    else:
        result = "Error: " + str(s)
        session['result'] = result
        return str(result)
    return "i walk the line"

@login.route('/user/<string:username>/update',methods=["GET","POST"])
def update(username):
	error=request.form["bingo"]
	transfer=redis_connect()
	transfer.rpush("error",error)
	return redirect('/user/'+username+'/masterquery')
   


login.run()
