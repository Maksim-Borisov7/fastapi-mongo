from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Request

from app.config import settings


class DataBaseHelper:
    def __init__(self, mongodb_url: str = f'mongodb://{settings.MONGO_HOST}:{settings.MONGO_PORT}'):
        self.client = AsyncIOMotorClient(mongodb_url)
        self.dbs = self.client[settings.MONGO_DB]

    def get_collection(self, collection: str):
        return self.dbs[collection]

    @staticmethod
    def get_db(request: Request):
        return request.app.state.db_helper




