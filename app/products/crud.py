import logging
from fastapi import HTTPException
from app.database.db_helper import DataBaseHelper


async def add_product_admin(data_product, db: DataBaseHelper):
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


async def get_products(db: DataBaseHelper):
    products = []
    try:
        collections = db.get_collection('products')
        async for product in collections.find():
            products.append(product)
        return products
    except Exception as err:
        raise HTTPException(status_code=400, detail=logging.info(err))


async def get_product(id: int, db: DataBaseHelper) -> dict:
    try:
        collections = db.get_collection('products')
        return await collections.find_one({"_id": int(id)})
    except Exception as err:
        raise HTTPException(status_code=400, detail=logging.info(err))


async def add_product_in_basket(product: dict, user, db: DataBaseHelper):
    try:
        collections = db.get_collection('users')
        await collections.update_one(
                                        {"_id": user["_id"]},
                                        {'$push': {"basket": product}}
                                        )
    except Exception as err:
        raise HTTPException(status_code=400, detail=logging.info(err))


async def update_product(update_data, data, db: DataBaseHelper):
    try:
        dict_update_data = dict(update_data)
        collections = db.get_collection('products')
        await collections.update_one(
            {"_id": data["_id"]},
            {"$set": dict_update_data}
        )
    except Exception as err:
        raise HTTPException(status_code=400, detail=logging.info(err))


async def delete_product(id, db: DataBaseHelper):
    try:
        collections = db.get_collection('products')
        await collections.delete_one({"_id": int(id)})
        return {'msg': 'Продукт успешно удалён'}
    except Exception as err:
        raise HTTPException(status_code=400, detail=logging.info(err))


async def delete_product_from_basket(id, user, db: DataBaseHelper):
    try:
        collections = db.get_collection('users')
        await collections.update_one(
                                    {"_id": user['_id']},
                                    {"$pull": {"basket": {"_id": int(id)}}}
                                    )
    except Exception as err:
        raise HTTPException(status_code=400, detail=logging.info(err))


async def buy_products(user, db: DataBaseHelper):
    try:
        collections_products = db.get_collection('products')
        for value in user['basket']:
            id = value['_id']
            product = await get_product(id, db)
            await collections_products.update_one(
                {'_id': id},
                {'$set': {"quantity": product['quantity'] - value['quantity']}}
            )
            await delete_product_from_basket(id, user, db)
        return {'msg': 'Ваш заказ оплачен'}
    except Exception as err:
        raise HTTPException(status_code=400, detail=logging.info(err))


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
