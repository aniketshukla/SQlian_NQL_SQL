from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash
import redis
import time

dashboard=Flask(__name__)
#alternative to config.py
DEBUG=True
SECRET_KEY='development key'
USERNAME='admin'
PASSWORD='default'
#config over
dashboard.config.from_object(__name__)

@dashboard.route("/pimp")
def pimp():
	return pimp