from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required 
# JWT= json web token --> encoding of data so that data is secure
# when client register, send them a JWT. Client sent us JWT for each request and we will be sure 
# they have previously been authenticated

from security import authenticate, identity # import the functions to check that user is in list 
from resources.users import UserRegister # import the resource class UserRegister to add api later 
# when importing from a python file in folder, user folder_name.filename

# import in items and item list 
from resources.item import Item, Items 

# import store and storelist
from resources.store import Store, StoreList
# import SQLAlchemy object
from db import db

app = Flask(__name__)

# tell SQLAlchemy where is the data.db file, which contains all the tables used in the app
# data.db will be created when running the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # sqlite refers to the current root folder

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # just remove tracking since another tracking is better
# create a secret key for the app, should be complex to ensure security
app.secret_key = 'cumulus'

# set up JWT to work with the app
# create JWT, and add in function to use for authentication, authenticate and identity function created earlier 
jwt = JWT(app, authenticate, identity) # JWT creates endpoint /auth, send username and password to /auth
# jwt send username and password to authenticate and identity function
# if the authentication function work properly return a jwt token, which will feed in to identity to check 

# create API 
api = Api(app)
# Resource is something API can create and return 
# API works with resources and every resource is a class
# create a new class that inherits from the class Resource 

# FIRST RESTFUL APP
# create a resource and the methods that resource can accept
# method must be http verb like get, post, delete 
# class Student(Resource):
#     # get method, name is name of student, return in json form
#     def get(self,name):
#         return {'student': name}

# # add resource to API and determine the http to access the API (endpoint)
# api.add_resource(Student, '/student/<string:name>') # eg http://127.0.0.1:5000/student/joe
# # run the app
# app.run(port=5000, debug = True)
# determine how the method would be assessed using the GET request statement


# PART 2: COMPLETE EXAMPLE FOR RESTFUL
# create two distinct resources (classes) item list and item since they have different properties
# not using database to store items for now, use a list of dictionaries where each item is a dictionary
# items_list = [
#     {'name':'apple', 'price':11.65}
# ]

########################
# create tables using SQLAlchemy instead of using sqlite3 to create table  
@app.before_first_request # decorator that affects method below it, this will run the method before first request
def create_table():
    db.create_all() # create all tables unless exists already, the tables are all specified under 
    # ItemModel and UserModel class that specific column properties and tables names

# add the resource into api
api.add_resource(Items, '/items') # eg http://127.0.0.1:5000/items
api.add_resource(Item, '/item/<string:name>') # same endpoint but different input in postman
# for get and post method  

api.add_resource(UserRegister, '/register') # add api for registering user 

# add store
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

# add this line to ensure that when importing app_with_sql file, the run app command would not be 
# executed and only execute this line when running the app file, since name will be __main__ when file is run 
if __name__ == '__main__':
    db.init_app(app) # activate SQLAlchemy to this app
    app.run(port=5000, debug=True)
# status code 404 for error in API, 202 is accepted but delay of creation

# filter(lambda x: x['name']==name, items), filter apply the lambda function to each item in items 
# returns a filter object, list(filter) would get a list of all items that match filter function 
# next(filter) return the first item found by filter function, since items should have unique names

# authentication
# get user from data base when /auth is called to check is user is registered in database before
# returning jwt token  