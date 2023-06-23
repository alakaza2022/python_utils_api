from pymongo import MongoClient

# MongoDB connection details
connection_string = 'mongodb+srv://popout:wl7S29Y1jZmJgw8v@popout-cluster.areun.mongodb.net/popout?retryWrites=true&w=majority'
database_name = 'popout'
collection_name = 'stores'

# Connect to MongoDB
client = MongoClient(connection_string)
database = client[database_name]
collection = database[collection_name]

# Aggregate pipeline to remove duplicate values
pipeline = [
    {"$group": {"_id": "$location", "count": {"$sum": 1}}},
    {"$match": {"count": {"$gt": 1}}}
]

# Iterate over duplicate values and update documents
duplicate_values = collection.aggregate(pipeline)
for value_doc in duplicate_values:
    value = value_doc['_id']
    duplicate_docs = collection.find({"location": value})
    first_doc = True
    for doc in duplicate_docs:
        if first_doc:
            first_doc = False
        else:
            collection.delete_one({"_id": doc['_id']})
            print(
                f"Deleted duplicate value '{value}' from document with _id: {doc['_id']}")

# Disconnect from MongoDB
client.close()
