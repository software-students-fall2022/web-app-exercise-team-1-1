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
cxn = pymongo.MongoClient(config['MONGO_URI'], username='admin', password ='secret') #need to include username and password to insert doc to database
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
    docs="Welcome Team 1 Members" #test if the website is working

    return render_template('index.html', docs=docs) # render the hone template

@app.route('/createEvent', methods=['POST', 'GET'])
def create_event():

    if request.method == 'POST':
        title = request.form['Title']
        summary = request.form['Summary']

        # create a new document with the data the user entered
        doc = {
            "Title": title,
            "Summary": summary, 
            "created_at": datetime.datetime.utcnow()
        }
        db.event.insert_one(doc) # insert a new document

    return render_template('create_new_event.html')

@app.route('/showEvent', methods=['POST', 'GET'])
def show_event():
    if request.method == 'GET':
        docs = db.event.find({}).sort("created_at", -1) # sort in descending order of created_at timestamp
    

    return render_template('show_event.html',docs=docs)  

@app.route('/deleteEvent/<event_id>')
def delete_event(event_id):
    """
    Route for GET requests to the delete page.
    Deletes the specified record from the database, and then redirects the browser to the home page.
    """
    db.event.delete_one({"_id": ObjectId(event_id)})
    return redirect(url_for('show_event')) # tell the web browser to make a request for the / route (the home function)

@app.route('/editEvent/<event_id>')
def edit2(event_id):
    #if request.method == 'GET':
        #list = db.membertest.find({}).sort("created_at", -1)
    doc = db.event.find_one({"_id": ObjectId(event_id)})
    
    return render_template('edit_event.html', doc=doc) # render the edit template


# route to accept the form submission to delete an existing post
@app.route('/editEvent/<event_id>', methods=['POST'])
def edit_event(event_id):
    if request.method == 'POST':
        title = request.form['Title']
        summary = request.form['Summary']

            # create a new document with the data the user entered
        doc = {
            "Title": title,
            "Summary": summary, 
            "Created_at": datetime.datetime.utcnow()
        }

        db.event.update_one(
            {"_id": ObjectId(event_id)}, # match criteria
            { "$set": doc }
        )

        #return render_template('editMember.html', doc=doc) 
        return redirect(url_for('show_event'))


@app.route('/createMember', methods=['POST', 'GET'])
def create_member():

    if request.method == 'POST':
        Name = request.form['Name']
        ContactInfo = request.form['ContactInfo']

        # create a new document with the data the user entered
        doc = {
            "Name": Name,
            "ContactInfo": ContactInfo, 
            "created_at": datetime.datetime.utcnow()
        }
        db.membertest.insert_one(doc) # insert a new document

    return render_template('create_new_member.html') 

@app.route('/showMember', methods=['POST', 'GET'])
def show_member():
    if request.method == 'GET':
        list = db.membertest.find({}).sort("created_at", -1) # sort in descending order of created_at timestamp
    

    return render_template('show_member.html',docs=list)  

@app.route('/editMember/<member_id>')
def edit(member_id):
    #if request.method == 'GET':
        #list = db.membertest.find({}).sort("created_at", -1)
    doc = db.membertest.find_one({"_id": ObjectId(member_id)})
    
    return render_template('editMember.html', doc=doc) # render the edit template


# route to accept the form submission to delete an existing post
@app.route('/editMember/<member_id>', methods=['POST'])
def edit_member(member_id):
    if request.method == 'POST':
        Name = request.form['Name']
        ContactInfo = request.form['ContactInfo']

        doc = {
            # "_id": ObjectId(post_id), 
            "Name": Name, 
            "ContactInfo": ContactInfo, 
            "created_at": datetime.datetime.utcnow()
        }

        db.membertest.update_one(
            {"_id": ObjectId(member_id)}, # match criteria
            { "$set": doc }
        )

        #return render_template('editMember.html', doc=doc) 
        return redirect(url_for('show_member'))


@app.route('/deleteMember/<member_id>')
def delete_member(member_id):

    db.membertest.delete_one({"_id": ObjectId(member_id)})
    return redirect(url_for('show_member'))

@app.route('/createPost', methods=['POST', 'GET'])
def create_post():

    if request.method == 'POST':
        title = request.form['title']
        theme = request.form['theme']
        date_location = request.form['date_location']
        summary = request.form['summary']


        # create a new document with the data the user entered
        doc = {
            "title": title,
            "theme": theme, 
            "created_at": datetime.datetime.utcnow(),
            "date_location": date_location, 
            "summary": summary
        }
        db.post.insert_one(doc) # insert a new document

    return render_template('create_new_post.html')

@app.route('/showPost', methods=['POST', 'GET'])
def show_post():
    if request.method == 'GET':
        docs = db.post.find({}).sort("created_at", -1) # sort in descending order of created_at timestamp
    
    return render_template('show_post.html',docs=docs)  

@app.route('/deletePost/<post_id>')
def delete_post(post_id):
    """
    Route for GET requests to the delete page.
    Deletes the specified record from the database, and then redirects the browser to the home page.
    """
    db.post.delete_one({"_id": ObjectId(post_id)})
    return redirect(url_for('show_post')) # tell the web browser to make a request for the / route (the home function)

@app.route('/editPost/<post_id>')
def edit3(post_id):
    #if request.method == 'GET':
        #list = db.membertest.find({}).sort("created_at", -1)
    doc = db.post.find_one({"_id": ObjectId(post_id)})
    
    return render_template('edit_post.html', doc=doc) # render the edit template

# route to accept the form submission to delete an existing post
@app.route('/editPost/<post_id>', methods=['POST'])
def edit_post(post_id):
    if request.method == 'POST':
        title = request.form['title']
        summary = request.form['summary']
        theme = request.form['theme']
        date_location = request.form['date_location']

            # create a new document with the data the user entered
        doc = {
            "title": title,
            "summary": summary, 
            "theme": theme,
            "date_location": date_location,
            "Created_at": datetime.datetime.utcnow()
        }

        db.post.update_one(
            {"_id": ObjectId(post_id)}, # match criteria
            { "$set": doc }
        )

        #return render_template('editMember.html', doc=doc) 
        return redirect(url_for('show_post'))