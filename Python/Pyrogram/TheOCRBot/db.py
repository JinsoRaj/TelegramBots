# (c) HYBRID
import os
from config import DATABASE_URI
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient


mongo_client = MongoClient(DATABASE_URI)
db = mongo_client.ocr
usersdb = db.users


async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True

async def add_served_user(user_id: int, message):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    await usersdb.insert_one({"user_id": user_id}, {"$set": {"user_count": 0}})
    return

async def user_ocr_count(user_id):
    user = await usersdb.find_one({"user_id": user_id})
    count_d = user.get("user_count")
    if count_d is None:
        count = 0
    else:
        count = count_d
    return count

async def add_user_ocr(user_id: int, message):
    user = await usersdb.find_one({"user_id": user_id})
    if user is not None:
        count = await user_ocr_count(user_id)
        new_count = count + 1
        usersdb.update_one({"user_id": user_id}, {"$set": {"user_count": new_count}})
    return

async def update_user_language(user_id, language_code):
    await usersdb.update_one({"user_id": user_id}, {"$set": {"user_lang": language_code}}, upsert=True)

async def user_lang(user_id):
    user = await usersdb.find_one({"user_id": user_id})
    lang_s = user.get("user_lang")
    if lang_s is None:
        lang = "eng"
    else:
        lang = lang_s
    return lang

async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list

async def get_total_use_count():
    total_count = 0
    async for user in usersdb.find():
        total_count += user.get("user_count", 0)
    return total_count

async def get_total_users_count():
    total_user_count = await usersdb.count_documents({})
    return total_user_count
