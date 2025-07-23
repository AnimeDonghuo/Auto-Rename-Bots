# /database/users_chats_db.py

from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URI, DB_NAME

# MongoDB client setup
client = AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]

# Collections
users_col = db["users"]
chat_modes_col = db["chat_modes"]

# Add user to DB
async def add_user(user_id):
    user = await users_col.find_one({"_id": user_id})
    if not user:
        await users_col.insert_one({"_id": user_id})

# Set upload mode (document/video)
async def add_upload_mode(user_id, mode):
    await chat_modes_col.update_one(
        {"_id": user_id},
        {"$set": {"upload_mode": mode}},
        upsert=True
    )

# Get upload mode
async def get_upload_mode(user_id):
    data = await chat_modes_col.find_one({"_id": user_id})
    return data.get("upload_mode", "document") if data else "document"
