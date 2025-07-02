from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from jwt.exceptions import InvalidTokenError

from app.database.db_helper import DataBase
from app.users.auth import decode_jwt
from app.users.crud import UsersDAO
from app.users.schemas import UsersAuthSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/authorization/')


async def get_token_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не валидный токен"
        )
    return payload


async def get_current_auth_user(payload: dict = Depends(get_token_payload),
                                db: DataBase = Depends(DataBase.get_db)):
    user_id = str(payload.get("sub"))
    user = await UsersDAO.get_user_by_id(user_id, db)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")


async def get_current_is_admin(current_user: UsersAuthSchema = Depends(get_current_auth_user)):
    if current_user['is_admin']:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')


async def get_current_is_user(current_user: UsersAuthSchema = Depends(get_current_auth_user)):
    if current_user['is_user']:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')
