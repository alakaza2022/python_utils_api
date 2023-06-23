from pkgutil import get_data
from pymongo import MongoClient


def get_database(db_name):
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = 'mongodb+srv://popout:wl7S29Y1jZmJgw8v@popout-cluster.areun.mongodb.net/popout?retryWrites=true&w=majority'

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[db_name]


def upload_to_bands_collection(item):
    db = get_database("popout")
    collection_name = db["bands"]
    collection_name.insert_one(item)


def get_all_bands():
    db = get_database("popout")
    collection_name = db["bands"]
    return collection_name.find({})


def get_all_stores():
    db = get_database("popout")
    collection_name = db["stores"]
    return collection_name.find({})
