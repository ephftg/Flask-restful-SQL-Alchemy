# create items data base
# code will need to change to connect api to data base without the usual list to store all items
 
from multiprocessing import connection
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.itemModel import ItemModel # replace all self by ItemModel since now item is a instance of a class 

# create and save API end points to try out in Postman first to know what to include in methods
# return the list of all items
class Items(Resource):
    def get(self):

        return {'items': [I.json() for I in ItemModel.query.all()]} # .all is to get all data in data base
        # apply json to all items to get in dictionary form so that it can be returned

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # all_items_query = "SELECT * FROM items"
        # result = cursor.execute(all_items_query)
        # # create a list containing all items
        # everything = []
        # for row in result:
        #     everything.append({'name': row[0], 'price':row[1]})
        
        # connection.close()
        # return {'items': everything}


# get/post/delete/put items, return item to inform application that the action is done  
class Item(Resource):

    # create parser as the class object so that any method in class can use it by using Item.parser
    # request parsing using reqparse: ensure that only what is required is extracted from json payload (input from postman)
    # returns a dictionary with required keys and values
    parser = reqparse.RequestParser() # create object to parse the request
    # set the key to be extracted, set the type, and the mesage if error occurs 
    parser.add_argument('price', type=float, required=True, help="Cannot be blank")

    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id")

    # use postman and get access_token of authorized user first using POST /auth by entering username,password
    # username and password pair must be in the user list 
    # 401 is unathorized, to use the get function, add authorization header in postman for jwt_rquired() method
    # value is "JWT xxx" where xxx is the access_token obatined from /auth method
    
    @jwt_required() # a decorator that needs to be before a function
    # if add jwt_required(), then need to authenticate before calling the method below
    # get information of item with name, by finding it in items table in data base else return error 
    def get(self,name):
        wanted_item = ItemModel.find_by_name(name)
        if wanted_item:
            return wanted_item.json() # so as to convert item object to dictionary to be read

        return {"message": 'Item not found'}, 404 # return if item not found, always return json
    
    # get method requires security password so other methods cannot use it and need to create other method

    # use try-except block to handle the exception when the code may have error, 500 is internal server error

    # use class method find_by_name to check if item already exist in data base, if not inside, add it in else error
    
    # ItemModel.find_by_name return ItemModel object
    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message': 'item {} already exists'.format(name)}
        
        data = Item.parser.parse_args() # get info from input
        adding_item = ItemModel(name, data['price'], data['store_id']) # convert to itemModel
        
        try: 
            adding_item.save_to_db() # insert item into data base by calling the insert method on itself

        except:
            return {"message": "An error occurred when inserting item"}, 500

        return adding_item.json(), 201 # 201 means object created in database

    # delete item method from data base using the name of item 
    def delete(self,name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # #update items table by setting new price where name matches the desired item
        # delete_item_query = "DELETE FROM items WHERE name=?" # need to specify the name else delete whole table
        # cursor.execute(delete_item_query, (name,)) 
        # connection.commit() # changes to data base so need commit
        # connection.close() # not using data base, so close it 
        # return {"message": 'Item deleted'}
        item_to_delete = ItemModel.find_by_name(name)
        if item_to_delete: # if item exist, delete it
            item_to_delete.delete_from_db()
        return {'message': 'Item deleted'}
        

    # put: update existing item or create item
    # check whether item exist, if exist update it else add new item in data base
    def put(self, name):
        # parse the input from the json payload to extract only wanted keys, the rest of the info in json payload is ignored
        data = Item.parser.parse_args()
        current_item = ItemModel.find_by_name(name)

        if current_item is None: # item does not exists yet, create item 
            current_item = ItemModel(name, data['price'], data['store_id'])
        else: # item exists, change the price
            current_item.price = data['price']
            current_item.store_id = data['store_id']
        
        # if price change, since item has unique id, SQLAlchmey will just update it
        # if does not exist, will add new item in data base
        current_item.save_to_db()

        return  current_item.json()

# get method, result should be unique
# retrieve item from data base using get method 