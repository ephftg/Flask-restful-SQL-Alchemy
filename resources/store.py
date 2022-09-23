
from flask_restful import Resource
from models.storeModel import StoreModel

class Store(Resource):
    # get store from name
    def get(self,name):
        wanted_store = StoreModel.find_by_name(name)
        if wanted_store:
            return wanted_store.json()
        
        return {'message': 'Store no found'}, 404

    
    # add store
    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message': "A store withn name {} already exist.".format(name)}, 400
        
        new_store = StoreModel(name)
        try:
            new_store.save_to_db()
        except:
            return {'message': "Error when saving store"}, 500
        
        return new_store.json(), 201
    
    # delete store
    def delete(self,name):
        store_delete = StoreModel.find_by_name(name)
        if store_delete:
            store_delete.delete_from_db()
        
        return {'message': "Store is deleted"}


# a dictionary of stores where each store is a json
class StoreList(Resource):
    def get(self):
        return {'Stores': [S.json() for S in StoreModel.query.all()]}

