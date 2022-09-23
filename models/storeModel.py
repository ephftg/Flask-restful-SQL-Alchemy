from db import db

# store is a store that contains the different items
class StoreModel(db.Model): 

    # tell SQLALchemy name of table associated to this model
    __tablename__ ='stores'

    # tell SQLALchemy the information about the columns of the table
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80)) # maximum 80 characters 

    # get the items that are in the store, this is extra column in the stores table 
    items = db.relationship("ItemModel", lazy='dynamic') # specify to join with item model, SQLAlchemy to go to ItemModel 
    # to see what is the relationship, which is specify by the Foreign key. Return a list of items 

    # each time a store is created, find all items that is linked to the store which can take a long time
    # set lazy=dynamic so  that self.items is not a property of StoreModel, but a query in SQLAlchemy 
    # so will not have items until json function for StoreModel called

    # when creating store input name
    def __init__(self, name): 
        self.name = name

    # json method that return json representation of store
    # self.items is a query, so use .all() to get all items from the query 
    # do the query each time json method is called, so can be slow to run 
    def json(self):
        return {'name': self.name, 'items': [I.json() for I in self.items.all()]}


    @classmethod # method act on itself 
    def find_by_name(cls,name):
        return StoreModel.query.filter_by(name=name).first()
        # .first() select the first row from the output. Returns a StoreModel 

   # add new store 
    def save_to_db(self):
        # session is a collect of objects that will be added to data base, can add multiple object each time
        db.session.add(self) # add self which is the ItemModel object into data base 
        db.session.commit() # commit to save the changes in data base

    # delete from data base
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
