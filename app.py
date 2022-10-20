from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import dotenv_values

import pymongo
import datetime
from bson.objectid import ObjectId
import sys


app = Flask(__name__)

config = dotenv_values(".env")
# turn on debugging if in development mode
#if config['FLASK_ENV'] == 'development':
    # turn on debugging, if in development
    #app.debug = True # debug mnode
# connect to the database
cxn = pymongo.MongoClient(config['MONGO_URI'], username='admin', password='secret') #need to include username and password to insert doc to database
try:
    # verify the connection works by pinging the database
    cxn.admin.command('ping') # The ping command is cheap and does not require auth.
    db = cxn[config['MONGO_DBNAME']] # store a reference to the database
    print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!
except Exception as e:
    # the ping command failed, so the connection is not available.
    # render_template('error.html', error=e) # render the edit template
    print(' *', "Failed to connect to MongoDB at", config['MONGO_URI'])
    print('Database connection error:', e) # debug

@app.route('/')
def home():
    """
    Route for the home page
    """
    #docs = db.exampleapp.find({}).sort("created_at", -1) # sort in descending order of created_at timestamp
    docs="hello world" #test if the website is working
    
    # for testing insertion of doc to database
    doc = {
        "name": "member1",
        "phone": 123456
    }
    db.member.insert_one(doc) # insert a member in database

    return render_template('index.html', docs=docs) # render the hone template