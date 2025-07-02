from typing import Annotated
from fastapi import APIRouter, Depends

from app.database.db_helper import DataBase
from app.dependencies import get_current_is_user
from app.products.crud import ProductsDAO
from app.products.schemas import AddProductInBasket
from app.users.schemas import UsersAuthSchema

router = APIRouter(prefix='/basket', tags=["Взаимодействие покупателя с корзиной"])


@router.post('/add_products/')
async def add_products_for_users(data_product: Annotated[AddProductInBasket, Depends()],
                                 current_user: UsersAuthSchema = Depends(get_current_is_user),
                                 db: DataBase = Depends(DataBase.get_db)):
    product = await ProductsDAO.get_product(data_product.id, db)
    if product["quantity"] - data_product.quantity < 1:
        return {'msg': 'Превышен лимит товаров'}
    if product is not None:
        product["quantity"] = data_product.quantity
        await ProductsDAO.add_product_in_basket(product, current_user, db)
        return {'msg': 'Продукт добавлен в корзину'}
    return {'msg': 'Данного продукта нет в наличии'}


@router.get('/get_products/all/users')
async def get_all_products(current_user: UsersAuthSchema = Depends(get_current_is_user),
                           db: DataBase = Depends(DataBase.get_db)):
    return await ProductsDAO.get_products(db)


@router.delete('/delete_products/{id}')
async def delete_products(id,
                          db: DataBase = Depends(DataBase.get_db),
                          current_user: UsersAuthSchema = Depends(get_current_is_user),):
    await ProductsDAO.delete_product_from_basket(id,
                                     current_user,
                                     db)
    return {'msg': 'Продукт был удален из вашей корзины'}


@router.post('/buy_products/')
async def make_order(db: DataBase = Depends(DataBase.get_db),
                     current_user: UsersAuthSchema = Depends(get_current_is_user),):
    return await ProductsDAO.buy_products(current_user, db)


@router.get('/my_basket/')
async def view_basket(current_user: UsersAuthSchema = Depends(get_current_is_user),):
    return await ProductsDAO.get_my_basket(current_user)

