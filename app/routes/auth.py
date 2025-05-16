import logging
from typing import Annotated
from fastapi import APIRouter, Depends

from app.database.db_helper import DataBaseHelper
from app.users.auth import hash_password, validate_auth_user, encode_jwt
from app.users.crud import get_user, add_user
from app.users.schemas import UsersRegistrationSchema, UsersAuthSchema, TokenInfo

router = APIRouter(prefix="/auth", tags=["Авторизация и аутенфтификация"])


@router.post('/registration', description="Регистрация пользователей",)
async def registration_users(credentials: Annotated[UsersRegistrationSchema, Depends()],
                             db: DataBaseHelper = Depends(DataBaseHelper.get_db)) -> dict:
    logging.info("Регистрация пользователя")
    user = await get_user(credentials.username, db)
    if user is None:
        hash_pwd = hash_password(credentials.password)
        user_dict = dict(credentials)
        user_dict['password'] = hash_pwd
        await add_user(user_dict, db)
        return {"msg": "Пользователь успешно зарегистрирован"}
    return {'msg': "Пользователь уже существует"}


@router.post('/authorization', description="Аутентификация пользователей", response_model=TokenInfo)
async def authorization_users(credentials: UsersAuthSchema = Depends(validate_auth_user),):
    logging.info("Авторизация пользователя")
    jwt_payload = {
        'sub': str(credentials['_id']),
        'username': credentials['username']
    }
    token = encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type='Bearer'
    )


