import logging
from fastapi import HTTPException
from app.database.db_helper import DataBaseHelper


async def get_user(username: str, db: DataBaseHelper):
    try:
        collection = db.get_collection('users')
        user = await collection.find_one({"username": username})
        return user
    except Exception as err:
        raise HTTPException(status_code=400, detail=logging.info(err))


async def get_user_by_id(id: str, db: DataBaseHelper):
    try:
        collection = db.get_collection('users')
        user = await collection.find_one({"_id": int(id)})
        return user
    except Exception as err:
        raise HTTPException(status_code=400, detail=logging.info(err))


async def add_user(credentials: dict, db: DataBaseHelper):
    try:
        collection = db.get_collection('users')
        id = await collection.count_documents({}) + 1
        await collection.insert_one(
            {"_id": id,
             "username": credentials['username'],
             'password': credentials['password'],
             'email': credentials['email'],
             'is_user': True,
             'is_admin': False,
             'basket': []
             })
    except Exception as err:
        raise HTTPException(status_code=400, detail=logging.info(err))


async def change_credentials(user, db: DataBaseHelper):
    try:
        collections = db.get_collection('users')
        await collections.update_one(
            {"_id": user['_id']},
            {"$set": {"is_user": False,
             'is_admin': True}}
        )
    except Exception as err:
        raise HTTPException(status_code=400, detail=logging.info(err))
