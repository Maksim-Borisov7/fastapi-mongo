from typing import Annotated
from fastapi import APIRouter, Depends

from app.database.db_helper import DataBaseHelper
from app.dependencies import get_current_is_admin
from app.products.crud import add_product_admin, get_products, update_product, get_product, delete_product
from app.products.schemas import ProductSchema
from app.users.schemas import UsersAuthSchema

router = APIRouter(prefix="/auth", tags=["Привелегии администратора"])


@router.post('/add_products/one')
async def add_products(data_product: Annotated[ProductSchema, Depends()],
                       current_user: UsersAuthSchema = Depends(get_current_is_admin),
                       db: DataBaseHelper = Depends(DataBaseHelper.get_db)):
    await add_product_admin(data_product, db)
    return {'msg': 'Продукт успешно добавлен админом'}


@router.get('/get_products/all/admin')
async def get_all_products(db: DataBaseHelper = Depends(DataBaseHelper.get_db),
                           current_user: UsersAuthSchema = Depends(get_current_is_admin)):
    return await get_products(db)


@router.get("/get_products/{id}")
async def get_product_by_id(id,
                            db: DataBaseHelper = Depends(DataBaseHelper.get_db),
                            current_user: UsersAuthSchema = Depends(get_current_is_admin)):
    product = await get_product(id, db)
    if product:
        return product
    return {'msg': f'Продукта с id: {id} не существует'}


@router.put('/update_products/{id}')
async def update_product_by_id(id,
                               update_data: Annotated[ProductSchema, Depends()],
                               current_user: UsersAuthSchema = Depends(get_current_is_admin),
                               db: DataBaseHelper = Depends(DataBaseHelper.get_db)):
    data_product = await get_product(id, db)
    await update_product(update_data, data_product, db)
    return {"msg": 'Данные успешно обновлены'}


@router.delete("/delete_products/{id}")
async def delete_products_by_id(id,
                                current_user: UsersAuthSchema = Depends(get_current_is_admin),
                                db: DataBaseHelper = Depends(DataBaseHelper.get_db),):
    return await delete_product(id, db)


@router.get('/get_all_users')
async def get_all_users(current_user: UsersAuthSchema = Depends(get_current_is_admin),
                        db: DataBaseHelper = Depends(DataBaseHelper.get_db)):
    collections = db.get_collection('users')
    lst = []
    async for user in collections.find():
        lst.append(user)
    return lst


