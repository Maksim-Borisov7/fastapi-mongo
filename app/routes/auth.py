import logging
from typing import Annotated
from fastapi import APIRouter, Depends

from app.database.db_helper import DataBase
from app.users.auth import validate_auth_user, encode_jwt
from app.users.crud import UsersRepository
from app.users.schemas import UsersRegistrationSchema, UsersAuthSchema, TokenInfo

router = APIRouter(prefix="/auth", tags=["Авторизация и аутенфтификация"])


@router.post('/registration', description="Регистрация пользователей",)
async def registration_users(credentials: Annotated[UsersRegistrationSchema, Depends()],
                             db: DataBase = Depends(DataBase.get_db)) -> dict:
    logging.info("Регистрация пользователя")
    user = await UsersRepository.get_user(credentials.username, db)
    if user is None:
        await UsersRepository.create_users(credentials, db)
    return {'msg': "Пользователь уже существует"}


@router.post('/authorization', description="Аутентификация пользователей", response_model=TokenInfo)
async def authorization_users(credentials: UsersAuthSchema = Depends(validate_auth_user),):
    logging.info("Авторизация пользователя")
    await UsersRepository.user_verification(credentials)


