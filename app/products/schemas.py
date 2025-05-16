from pydantic import BaseModel


class AddProductInBasket(BaseModel):
    id: int
    quantity: int


class ProductSchema(BaseModel):
    name: str
    price: float
    descr: str
    quantity: int


