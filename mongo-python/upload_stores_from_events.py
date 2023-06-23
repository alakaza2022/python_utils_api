from pymongo import MongoClient

# MongoDB connection details

connection_string = 'mongodb+srv://popout:wl7S29Y1jZmJgw8v@popout-cluster.areun.mongodb.net/popout?retryWrites=true&w=majority'
source_db_name = 'popout'
source_collection_name = 'events'
destination_db_name = 'popout'
destination_collection_name = 'stores'

# Connect to MongoDB
client = MongoClient(connection_string)
source_db = client[source_db_name]
source_collection = source_db[source_collection_name]
destination_db = client[destination_db_name]
destination_collection = destination_db[destination_collection_name]

seen = {}
# Retrieve all documents from the source collection
documents = destination_collection.find({})
print(documents)
# Iterate over the documents and extract the "store" objects
count = 0
for document in documents:
    count += 1
    # print("hello")
    # store = document.get("store", {})
    # if "_id" in store and "location" in store:
    #     del store["_id"]
    #     if store["location"] in seen:
    #         continue
    #     seen[store["location"]] = 1
    # else:
    #     continue
    # # Insert each store object into the destination collection
    # destination_collection.insert_one(store)
    # print(f"Inserted store: {store}")
print(count)
# Disconnect from MongoDB
client.close()
