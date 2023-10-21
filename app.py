from flask import Flask

app=Flask(__name__)

from controller import *

@app.route("/")
def welcome():
    return "<b> Welcome to first API hello</b>"