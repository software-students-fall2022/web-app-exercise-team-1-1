import pymongo
from bson.objectid import ObjectId
import datetime

# make a connection to the database server
connection = pymongo.MongoClient("your_db_host", 27017,
                                username="your_db_username",
                                password="your_db_password",
                                authSource="your_db_name")
# select a specific database on the server
db = connection["your_db_name"]

config = dotenv_values()