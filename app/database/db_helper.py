from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Request


class DataBaseHelper:
    def __init__(self, mongodb_url: str = 'mongodb://localhost:27017'):
        self.client = AsyncIOMotorClient(mongodb_url)
        self.dbs = self.client['shop']

    def get_collection(self, collection: str):
        return self.dbs[collection]

    @staticmethod
    def get_db(request: Request):
        return request.app.state.db_helper




