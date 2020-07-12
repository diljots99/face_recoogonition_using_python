import pymongo
from pymongo import MongoClient



class MyDatabase():
    def __init__(self):
        try:
           
            client = MongoClient(port=27017)
        
           
        except :
             print("Exception in db Conection")
        self.myDb = client["face_recogonition"]

    def list_all_collection(self):
        return self.myDb.collection_names()


    def get_new_insert_id(self,collectionName):
        collection = self.myDb[collectionName]
        if collection.count():
            docs = collection.find().sort("_id",-1).limit(1)
            for  doc in docs:
                ID = doc["_id"]
                ID += 1
                return ID
        else:
            return 0

    def insert_user_data(self,collectionName,userData):
        collection = self.myDb[collectionName]
        collection.insert(userData)
    
    def get_user_data(self,collectionName,ID):
        collection = self.myDb[collectionName]
        query ={
            '_id': ID
        }

        doc = collection.find_one(query)
        return doc

class MySqlDatabase():
    def __init__(self):
        try:
           
            client = MongoClient(port=27017)
            db = client.test
           
        except :
             print("Exception in db Conection")
        self.myDb = client["face_recogonition"]

    def list_all_collection(self):
        return self.myDb.collection_names()


    def get_new_insert_id(self,collectionName):
        collection = self.myDb[collectionName]
        if collection.count():
            docs = collection.find().sort("_id",-1).limit(1)
            for  doc in docs:
                ID = doc["_id"]
                ID += 1
                return ID
        else:
            return 0

    def insert_user_data(self,collectionName,userData):
        collection = self.myDb[collectionName]
        collection.insert(userData)
    
    def get_user_data(self,collectionName,ID):
        collection = self.myDb[collectionName]
        query ={
            '_id': ID
        }

        doc = collection.find_one(query)
        return doc