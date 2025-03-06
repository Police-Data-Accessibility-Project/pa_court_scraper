from pymongo import MongoClient

# Connect to MongoDB running inside Docker

def get_collection(db_name: str = "mydatabase", collection_name: str = "mycollection"):
    mongo_uri = "mongodb://host.docker.internal:27017/"  # Use localhost since the container exposes the port
    client = MongoClient(mongo_uri)
    db = client[db_name]

    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)

    collection = db[collection_name]
    return collection


def insert_into_mongodb(
    content: dict
):
    collection = get_collection()
    # Insert a document
    collection.insert_one(content)

def print_contents():
    collection = get_collection()
    # Retrieve and print documents
    for doc in collection.find():
        print(doc)


if __name__ == "__main__":
    print_contents()