import logging
from typing import Annotated
from fastapi import APIRouter, Depends
from app.database.db_helper import DataBase
from app.dependencies import validate_auth_user
from app.users.schemas import UsersRegistrationSchema, UsersAuthSchema, TokenInfo
from app.users.use_case import AuthUseCase

router = APIRouter(prefix="/auth", tags=["Авторизация и аутенфтификация"])


@router.post('/registration', description="Регистрация пользователей",)
async def registration_users(credentials: Annotated[UsersRegistrationSchema, Depends()],
                             db: DataBase = Depends(DataBase.get_db)) -> dict:
    logging.info("Регистрация пользователя")
    return await AuthUseCase.register(credentials, db)


@router.post('/authorization', description="Аутентификация пользователей", response_model=TokenInfo)
async def authorization_users(credentials: UsersAuthSchema = Depends(validate_auth_user),):
    logging.info("Авторизация пользователя")
    return await AuthUseCase.user_verification(credentials)


