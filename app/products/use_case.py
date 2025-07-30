from app.products.crud import ProductsRepository


class ProductUseCase:
    @staticmethod
    async def send_product(product_id, db):
        product = await ProductsRepository.get_product(product_id, db)
        if product:
            return product
        return {'msg': f'Продукта с id: {product_id} не существует'}

    @staticmethod
    async def update_product(product_id, update_data, db):
        data_product = await ProductsRepository.get_product(product_id, db)
        if data_product is None:
            return {"msg": 'Введите данные'}
        await ProductsRepository.update_product(update_data, data_product, db)
        return {"msg": 'Данные успешно обновлены'}

    @staticmethod
    async def add_product(data_product, current_user, db):
        product = await ProductsRepository.get_product(data_product.id, db)
        if product["quantity"] - data_product.quantity < 1:
            return {'msg': 'Превышен лимит товаров'}
        if product is not None:
            product["quantity"] = data_product.quantity
            await ProductsRepository.add_product_in_basket(product, current_user, db)
            return {'msg': 'Продукт добавлен в корзину'}
        return {'msg': 'Данного продукта нет в наличии'}