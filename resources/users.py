# create user as a class to make it easier to creater user instead of creating many dictionaries

# LINK TO SQLITE DATA BASE
# add class method to allow User class to interact with sqlite database
# method to check if input username is in data base

import sqlite3
from flask_restful import Resource, reqparse
from models.userModel import UserModel # use user model
# REGISTERING user to sign up using the api /register, /register will add user to user data base

# create a class which is a resource, then only one method post to add user to data base
class UserRegister(Resource):
    # create parser which belongs to class to only get relevant data in from input when registering user
    parser = reqparse.RequestParser()
    # tell parser to get username variable, help is the statement when is empty
    parser.add_argument('username', type=str, required=True, help='This field cannot be blank')
    # same to get password
    parser.add_argument('password', type=str, required=True, help='This field cannot be blank')

    # post method 
    def post(self):
        data = UserRegister.parser.parse_args() # get the input inserted when user use the post method

        # check whether user has been registered before to prevrnt registering the same user twice
        if UserModel.find_by_username(data['username']):
            return {"message": "This usename has been registered"}, 400 # error

        # # if user not registerd before, add to data base
        # connection = sqlite3.connect('data.db') # connect to data base 
        # cursor = connection.cursor()

        # insert_query = "INSERT INTO users VALUES (NULL, ?, ?)" # id is automatically increasing so put NULL
        # cursor.execute(insert_query, (data['username'], data['password']))

        # connection.commit() # add input to table to need commit
        # connection.close()

        # create user and save it in 
        new_user = UserModel(data['username'], data['password'])
        new_user.save_to_db()

        return {"message": "New user created"}, 201