from typing import Annotated
from fastapi import APIRouter, Depends
from app.database.db_helper import DataBase
from app.dependencies import get_current_is_admin
from app.products.crud import ProductsRepository
from app.products.schemas import ProductSchema
from app.products.use_case import ProductUseCase
from app.users.crud import UsersRepository
from app.users.schemas import UsersAuthSchema

router = APIRouter(prefix="/auth", tags=["Привелегии администратора"])


@router.post('/add_products/one')
async def add_products(data_product: Annotated[ProductSchema, Depends()],
                       current_user: UsersAuthSchema = Depends(get_current_is_admin),
                       db: DataBase = Depends(DataBase.get_db)):
    await ProductsRepository.add_product_admin(data_product, db)
    return {'msg': 'Продукт успешно добавлен админом'}


@router.get('/get_products/all/')
async def get_all_products(db: DataBase = Depends(DataBase.get_db),
                           current_user: UsersAuthSchema = Depends(get_current_is_admin)):
    return await ProductsRepository.get_products(db)


@router.get("/get_products/{id}")
async def get_product_by_id(product_id,
                            db: DataBase = Depends(DataBase.get_db),
                            current_user: UsersAuthSchema = Depends(get_current_is_admin)):
    return await ProductUseCase.send_product(product_id, db)


@router.put('/update_products/{id}')
async def update_product_by_id(product_id,
                               update_data: Annotated[ProductSchema, Depends()],
                               current_user: UsersAuthSchema = Depends(get_current_is_admin),
                               db: DataBase = Depends(DataBase.get_db)):
    return await ProductUseCase.update_product(product_id, update_data, db)


@router.delete("/delete_products/{id}")
async def delete_products_by_id(product_id,
                                current_user: UsersAuthSchema = Depends(get_current_is_admin),
                                db: DataBase = Depends(DataBase.get_db),):
    return await ProductsRepository.delete_product(product_id, db)


@router.get('/get_all_users')
async def get_all_users(current_user: UsersAuthSchema = Depends(get_current_is_admin),
                        db: DataBase = Depends(DataBase.get_db)):
    return await UsersRepository.get_users(db)


