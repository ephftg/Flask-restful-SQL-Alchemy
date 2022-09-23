# model : internal representation of entity, things programmer use to help make code easier
# this allow coder to edit things that would not affect API directly
# API deals with resources, resource is external representation of an entity, client(web/mobile app) interact with API

# create UserModel and ItemModel class to use them, since they are not resources
# change the methods to be methods for the object and not class method 
# add json method to turn item to a json output 
# always test code to make sure all is working fine before adding new code 

# make resource to have only 4 method, get, put, delete and post method so that is the api calls that will change

import sqlite3
from db import db
class UserModel(db.Model):

    # tell SQLALchemy where tables would be stored, UserModel are stored in table users
    __tablename__ ='users' # name of users table in data.db
    
    # tell SQLALchemy the information about the columns of the table, so that it ignores other variables
    id = db.Column(db.Integer, primary_key = True) # type and it is primary key which is unique index for each user
    username = db.Column(db.String(80)) # maximum 80 characters 
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        #self.id = id
        self.username = username
        self.password = password

    # is a class method since method call the __init__ method from user class itself, so relace self with cls
    # get user from database using the username
    # will be use in authenticate function in security
    @classmethod
    def find_by_username(cls,username):
        # connection = sqlite3.connect('data.db') # create connection to database and create cursor
        # cursor = connection.cursor()

        # # SELECT * FROM users: query line that select all rows in database
        # # WHERE username=? in query line filters the result where username=?
        # # input for ? will be specified in execute line, input always in tuple form even for 1 input
        # query_username = "SELECT * FROM users WHERE username=?"
        # result = cursor.execute(query_username, (username, ))
        # row = result.fetchone() # .fetchone() to get first row of the output, else return None

        # if row:
        #     found_user = cls(row[0], row[1], row[2]) # create user using data base data 
        # else:
        #     found_user = None

        # connection.close() # close connection once method is done 
        # return found_user

        # code easier with SQLAlchemy
        return UserModel.query.filter_by(username=username).first()

    # similar class method but now get user from id
    # will be use in identity function in security  
    @classmethod
    def find_by_id(cls,input_id):
        # connection = sqlite3.connect('data.db') # create connection to database and create cursor
        # cursor = connection.cursor()

        # # SELECT * FROM users: query line that select all rows in database
        # # WHERE username=? in query line filters the result where username=?
        # # input for ? will be specified in execute line, input always in tuple form even for 1 input
        # query_id = "SELECT * FROM users WHERE id=?"
        # result = cursor.execute(query_id, (input_id, ))
        # row = result.fetchone() # .fetchone() to get first row of the output, else return None

        # if row:
        #     found_user = cls(row[0], row[1], row[2]) # create user using data base data 
        # else:
        #     found_user = None
        
        # connection.close()
        # return found_user

        # code using SQLAlchemy
        return UserModel.query.filter_by(id=input_id).first()
    
    # save user to users table
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
