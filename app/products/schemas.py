from pydantic import BaseModel, Field


class AddProductInBasket(BaseModel):
    id: int
    quantity: int = Field(gt=0)


class ProductSchema(BaseModel):
    name: str = Field(max_length=20)
    price: float = Field(gt=0)
    descr: str = Field(max_length=100)
    quantity: int = Field(gt=0)


