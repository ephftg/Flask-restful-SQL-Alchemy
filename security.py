from models.userModel import UserModel # import User class to use
from werkzeug.security import safe_str_cmp # import safe string compare to compare string

# from models.user import UserModel

# contain a list of registered users, which is like a data base
# users = [
#     User(1, 'alice', 'rabbithole')
# ]

# create a dictionary of mapping by username, id to the dictionary of the users
# this would grow according with the users data base
# easier to find the all users info using one variable
# username_map = {u.username:u for u in users}
# id_map = {u.id:u for u in users}


# CHANGES 
# list of user not needed anymore as users are all stored in database users 
# authenticate and identify function use user class method to check if input username and id belongs in database

# authenticate function called when /auth to check that username and password is in our list of users, return user if is
# check if user is in database using user class function with the username input, if not return None as default
# return user which will be use to generate jwt token 
def authenticate(username, password):
    wanted_user = UserModel.find_by_username(username) # get user if username in database
    if wanted_user and safe_str_cmp(wanted_user.password, password):
        return wanted_user

# compare string may have error in python, so use safe_str_cmp = safe string compare from flask 
# return true if strings are the same

# identity function take in payload
# used when request an endpoint that requires authentication, payload is input in 
def identity(payload): # payload is the user that is returned from the JWT output that test authenticate
    user_id = payload['identity'] # get user id from payload
    return UserModel.find_by_id(user_id) # get user that matches the user id obtained