import logging
from fastapi import HTTPException
from app.database.db_helper import DataBase
from app.products.schemas import ProductSchema


class ProductsDAO:
    @staticmethod
    async def add_product_admin(data_product: ProductSchema, db: DataBase):
        try:
            collections = db.get_collection('products')
            id = await collections.count_documents({}) + 1
            await collections.insert_one({"_id": id,
                                          'name': data_product.name,
                                          'price': data_product.price,
                                          'decr': data_product.descr,
                                          'quantity': data_product.quantity})
        except Exception as err:
            raise HTTPException(status_code=400, detail=logging.info(err))

    @staticmethod
    async def get_products(db: DataBase):
        products = []
        try:
            collections = db.get_collection('products')
            async for product in collections.find():
                products.append(product)
            return products
        except Exception as err:
            raise HTTPException(status_code=400, detail=logging.info(err))

    @staticmethod
    async def get_product(id: int, db: DataBase) -> dict:
        try:
            collections = db.get_collection('products')
            return await collections.find_one({"_id": int(id)})
        except Exception as err:
            raise HTTPException(status_code=400, detail=logging.info(err))

    @staticmethod
    async def add_product_in_basket(product: dict, user, db: DataBase):
        try:
            collections = db.get_collection('users')
            await collections.update_one(
                                            {"_id": user["_id"]},
                                            {'$push': {"basket": product}}
                                            )
        except Exception as err:
            raise HTTPException(status_code=400, detail=logging.info(err))

    @staticmethod
    async def update_product(update_data: ProductSchema, data: dict, db: DataBase):
        try:
            dict_update_data = dict(update_data)
            collections = db.get_collection('products')
            await collections.update_one(
                {"_id": data["_id"]},
                {"$set": dict_update_data}
            )
        except Exception as err:
            raise HTTPException(status_code=400, detail=logging.info(err))

    @staticmethod
    async def delete_product(id, db: DataBase):
        try:
            collections = db.get_collection('products')
            await collections.delete_one({"_id": int(id)})
            return {'msg': 'Продукт успешно удалён'}
        except Exception as err:
            raise HTTPException(status_code=400, detail=logging.info(err))

    @staticmethod
    async def delete_product_from_basket(id, user, db: DataBase):
        try:
            collections = db.get_collection('users')
            await collections.update_one(
                                        {"_id": user['_id']},
                                        {"$pull": {"basket": {"_id": int(id)}}}
                                        )
        except Exception as err:
            raise HTTPException(status_code=400, detail=logging.info(err))

    @classmethod
    async def buy_products(cls, user, db: DataBase):
        try:
            collections_products = db.get_collection('products')
            for value in user['basket']:
                id = value['_id']
                product = await cls.get_product(id, db)
                await collections_products.update_one(
                    {'_id': id},
                    {'$set': {"quantity": product['quantity'] - value['quantity']}}
                )
                await cls.delete_product_from_basket(id, user, db)
            return {'msg': 'Ваш заказ оплачен'}
        except Exception as err:
            raise HTTPException(status_code=400, detail=logging.info(err))

    @staticmethod
    async def get_my_basket(user):
        try:
            lst = []
            for product in user['basket']:
                lst.append(product)
            if len(lst) == 0:
                return {'msg': 'Ваша корзина пуста'}
            return lst
        except Exception as err:
            raise HTTPException(status_code=400, detail=logging.info(err))
