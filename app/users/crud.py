import logging
from fastapi import HTTPException
from app.database.db_helper import DataBase


class UsersRepository:
    @staticmethod
    async def get_user(username: str, db: DataBase):
        try:
            collection = db.get_collection('users')
            user = await collection.find_one({"username": username})
            return user
        except Exception as err:
            raise HTTPException(status_code=400, detail=logging.info(err))

    @staticmethod
    async def get_users(db):
        collections = db.get_collection('users')
        lst = []
        async for user in collections.find():
            lst.append(user)
        return lst

    @staticmethod
    async def get_user_by_id(product_id: str, db: DataBase):
        try:
            collection = db.get_collection('users')
            user = await collection.find_one({"_id": int(product_id)})
            return user
        except Exception as err:
            raise HTTPException(status_code=400, detail=logging.info(err))

    @staticmethod
    async def add_user(credentials: dict, db: DataBase):
        try:
            collection = db.get_collection('users')
            user_id = await collection.count_documents({}) + 1
            await collection.insert_one(
                {"_id": user_id,
                 "username": credentials['username'],
                 'password': credentials['password'],
                 'email': credentials['email'],
                 'is_user': True,
                 'is_admin': False,
                 'basket': []
                 })
        except Exception as err:
            raise HTTPException(status_code=400, detail=logging.info(err))

    @staticmethod
    async def change_credentials(user, db: DataBase):
        try:
            collections = db.get_collection('users')
            await collections.update_one(
                {"_id": user['_id']},
                {"$set": {"is_user": False,
                 'is_admin': True}}
            )
        except Exception as err:
            raise HTTPException(status_code=400, detail=logging.info(err))
