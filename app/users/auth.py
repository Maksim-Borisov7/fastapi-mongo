from datetime import timezone, datetime
import bcrypt
from datetime import timedelta
from app.config import settings
from jose import jwt


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str,
                      hashed_password: bytes
                      ) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


def encode_jwt(payload: dict,
               private_key=settings.private_key_path.read_text(),
               algorithm=settings.algorithm,
               expire_minutes: int = settings.access_token_expire_minutes,
               expire_timedelta: timedelta | None = None,
             ):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm
    )
    return encoded


def decode_jwt(token: str | bytes,
               public_key: str = settings.public_key_path.read_text(),
               algorithm: str = settings.algorithm):
    decoded = jwt.decode(token,
                         public_key,
                         algorithm
                         )
    return decoded




