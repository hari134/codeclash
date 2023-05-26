from pymongo import MongoClient
from urllib.parse import quote_plus

PASSWORD = "Password@123"
password = quote_plus(PASSWORD)

uri = f"mongodb+srv://mailtohari134:{password}@cluster0.1xkbb9l.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

db = client['codeclash']

def get_collection(collection_name : str):
    return db[collection_name]