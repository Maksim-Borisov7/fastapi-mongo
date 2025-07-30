import logging
from fastapi import HTTPException
from app.database.db_helper import DataBase
from app.users.auth import hash_password, encode_jwt
from app.users.schemas import TokenInfo


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
    async def get_user_by_id(id: str, db: DataBase):
        try:
            collection = db.get_collection('users')
            user = await collection.find_one({"_id": int(id)})
            return user
        except Exception as err:
            raise HTTPException(status_code=400, detail=logging.info(err))

    @staticmethod
    async def add_user(credentials: dict, db: DataBase):
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

    @classmethod
    async def create_users(cls, credentials, db):
        hash_pwd = hash_password(credentials.password)
        user_dict = dict(credentials)
        user_dict['password'] = hash_pwd
        await cls.add_user(user_dict, db)
        return {"msg": "Пользователь успешно зарегистрирован"}

    @staticmethod
    async def user_verification(credentials):
        jwt_payload = {
            'sub': str(credentials['_id']),
            'username': credentials['username']
        }
        token = encode_jwt(jwt_payload)
        return TokenInfo(
            access_token=token,
            token_type='Bearer'
        )
