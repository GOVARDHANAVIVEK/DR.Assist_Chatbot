from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
database_name = os.getenv("DATABASE_NAME")
collection_name = os.getenv("COLLECTION_NAME")
collection =""
try:
# Establish a connection to the MongoDB server
    client = MongoClient(mongo_uri,
                         ssl=True,
                         tls=True,
                         tlsAllowInvalidCertificates=True)
    # Access the database
    db = client[database_name]
    # Access a collection
    collection = db[collection_name]
    print(f" connected to mongo client.....")
except Exception as e:
    print(f"error : {e}")    



