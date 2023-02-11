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
    return redirect(url_for("visualizzaTerreni"))

@app.route("/test")
def prova():
    return render_template("p.html")

