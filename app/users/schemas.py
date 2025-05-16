from pydantic import BaseModel, Field, EmailStr


class UsersAuthSchema(BaseModel):
    username: str = Field(min_length=3, max_length=10)
    password: str = Field(min_length=3, max_length=10)


class UsersRegistrationSchema(UsersAuthSchema):
    email: EmailStr


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
