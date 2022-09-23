
# each resource should only have the api methods like get, post, delete and put 
# methods that clients do not interact with should be removed and group into a models

from db import db

# item is internal representation of an item, so need the same properties of item: name and price
class ItemModel(db.Model): # ItemModel extents SQLAlchemy so that the class ItemModel can save and retrieve from database
    
    # tell SQLALchemy where tables would be stored, ItemModel are stored in table items
    __tablename__ ='items' # name of items table in data.db

    # tell SQLALchemy the information about the columns of the table
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80)) # maximum 80 characters 
    price = db.Column(db.Float(precision=2)) # set to 2 decimal point

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id') ) # match to id from StoreModel
    # ForeignKey specify the column that it needs to match to, which is id column of stores table
    # due to the link between item object and store object, to delete store, need to delete all items 
    # related to it first, or change their store reference

    # add the property store to the item
    store = db.relationship('StoreModel') # same function as join, find store that matches the store id

    # when creating item input name and price of item
    def __init__(self, name, price, store_id): 
        self.name = name
        self.price = price
        self.store_id = store_id

    # json method that return json representation of item 
    def json(self):
        return {'name': self.name, 'price':self.price}

    # return ItemModel and not dictionary anymore since item is a ItemModel 
    # SQLAlchemy helps to simplify code to find items from table, return object directly and not just a row
    @classmethod
    def find_by_name(cls,name):
        # code without SQLAlchemy extension
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # find_item_query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(find_item_query, (name,))
        # row = result.fetchone() # should have only one item that matches the name, else none
        # connection.close() # not using data base, so close it 
        # if row:
        #     return cls(row[0],row[1]) # create a item by inputing name and price, since cls calls __init__ method
        
        # query statement using SQLAlchemy that returns a ItemModel directly 
        # .query is from extension from db.Model which is SQLAlchemy. 
        # It makes a query on the data base (items table which is specified by __tablename__, by filtering by name
        # can keep adding .filter_by(var=xxx) to the query if there is more conditions
        return ItemModel.query.filter_by(name=name).first()
        # .first() select the first row from the output. Returns a ItemModel object 

    # no longer class methods, change the methods so that the item acts on itself

    # insert/update item into the data base
    # same code for update because SQLAlchemy will automatically update item with unique Id 
    def save_to_db(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # insert_item_query = "INSERT INTO items VALUES (?,?)"
        # cursor.execute(insert_item_query, (self.name, self.price))
        # connection.commit() # changes to data base so need commit
        # connection.close() # not using data base, so close it 

        # session is a collect of objects that will be added to data base, can add multiple object each time
        db.session.add(self) # add self which is the ItemModel object into data base 
        db.session.commit() # commit to save the changes in data base
        
        # previous code without SQLAlchemy for update
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # #update items table by setting new price where name matches the desired item
        # update_item_query = "UPDATE items SET price=? WHERE name=?"
        # cursor.execute(update_item_query, (self.price, self.name)) # input for query should be in order of ? 
        # connection.commit() # changes to data base so need commit
        # connection.close() # not using data base, so close it 

    # delete from data base
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
