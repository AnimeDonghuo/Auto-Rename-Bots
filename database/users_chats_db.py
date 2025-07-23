import pymongo
from config import DB_URL

client = pymongo.MongoClient(DB_URL)
db = client['AutoRenameBot']
users_collection = db['users']

def add_user(user_id):
    users_collection.update_one(
        {"_id": user_id}, {"$set": {"upload_mode": "doc"}}, upsert=True
    )

def add_upload_mode(user_id, mode):
    users_collection.update_one(
        {"_id": user_id}, {"$set": {"upload_mode": mode}}, upsert=True
    )

def get_upload_mode(user_id):
    user = users_collection.find_one({"_id": user_id})
    return user.get("upload_mode", "doc") if user else "doc"
