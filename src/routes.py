from flask import redirect, url_for, render_template
from flask import request
from src import app
import logging

#Simple logger for debug
logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger
handler = logging.FileHandler('test.log') # creates handler for the log file
logger.addHandler(handler) # adds handler to the werkzeug WSGI logger

"""
    In this file we define all the routes of our website
"""

@app.route("/")
def homepage():
    return render_template("index.html")
@app.route("/login")
def loginPage():
    return render_template("login.html", cssfile=url_for("static",filename = "style.css"))
