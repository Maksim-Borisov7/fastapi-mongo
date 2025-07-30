from app.database.db_helper import DataBase
from app.users.auth import hash_password, encode_jwt
from app.users.crud import UsersRepository
from app.users.schemas import TokenInfo


class AuthUseCase:
    @classmethod
    async def register(cls, credentials, db: DataBase):
        user = await UsersRepository.get_user(credentials.username, db)
        if user is None:
            return await cls.registration_users(credentials, db)
        return {'msg': "Пользователь уже существует"}

    @staticmethod
    async def registration_users(credentials, db):
        hash_pwd = hash_password(credentials.password)
        user_dict = dict(credentials)
        user_dict['password'] = hash_pwd
        await UsersRepository.add_user(user_dict, db)
        return {"msg": "Пользователь успешно зарегистрирован"}

    @staticmethod
    async def user_verification(credentials):
        jwt_payload = {
            'sub': str(credentials['_id']),
            'username': credentials['username']
        }
        token = encode_jwt(jwt_payload)
        return TokenInfo(
            access_token=token,
            token_type='Bearer'
        )
