from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import dotenv_values

import pymongo
import datetime
from bson.objectid import ObjectId
import sys

app = Flask(__name__)

#config = dotenv_values(".env")

# turn on debugging if in development mode
#if config['FLASK_ENV'] == 'development':
    # turn on debugging, if in development
    #app.debug = True # debug mnode

@app.route('/')
def home():
    """
    Route for the home page
    """
    #docs = db.exampleapp.find({}).sort("created_at", -1) # sort in descending order of created_at timestamp
    docs="hello world"
    return render_template('index.html', docs=docs) # render the hone template
