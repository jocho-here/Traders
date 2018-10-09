from flask import request
import re
import json

# This is where utility functions reside
# For example, checking whether tables are there and resetting them and etc.

# Receive request data
def get_req_data():
    req = None

    if len(request.form) > 0:
        # Postman
        # request.data is empty with Postman
        print("Getting data from request.form")
        req = request.form
    elif len(request.data) > 0:
        # React
        # request.form is empty with react
        print("Getting data from request.data")
        req = json.loads(request.data.decode("utf-8"))

    return req


## DB related
# Creating tables if not found
def create_tables():
    print("create_tables")

# Creating new traders database if not existing
def create_new_database():
    print("create_new_database")

# DB health check
def db_checks():
    print("db_checks")
    #if database does not exist
    #   create_new_database()
    #
    #create_tables()

# Cleaning up database connections
def db_close():
    print("db_close")

# Totally resetting database
def reset_db():
    print("reset_db")
    #if not database_exists(get_db_url()):
    #    create_new_database()
    #
    #erase_tables()
    #create_tables()
