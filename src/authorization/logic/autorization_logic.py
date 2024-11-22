from fastapi import Request, HTTPException, status

from settings import authjwt
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from authorization.schemas import AccessTokenSchema, RefreshTokenSchema, UserSchema

class AUThLogic:
    def __init__(self):
        self.pwd_context = CryptContext(schemes={"bcrypt"}, deprecated="auto")

    def password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify(self, password: str, password_hash: str) -> bool:
        return self.pwd_context.verify(password, password_hash)

    @staticmethod
    def get_user(request: Request) -> UserSchema:
        if not hasattr(request.state, "user"):
            raise HTTPException(status_code=401, detail="User not authenticated")
        usr = request.state.user
        schema = UserSchema(user_id=usr.get("user_id"), role=usr.get("role"), email="")
        return schema


class JWTLogic:

    @staticmethod
    def __create_token(token_data: AccessTokenSchema | RefreshTokenSchema, expire: datetime):
        data = token_data.model_dump()
        data["expire"] = expire.isoformat()
        encode_jwt = jwt.encode(data, authjwt.authjwt_private_key, algorithm=authjwt.authjwt_algorithm)
        return encode_jwt

    @staticmethod
    def __decode_token(token: str, token_type: str) -> dict:
        try:
            payload = jwt.decode(token, authjwt.authjwt_private_key, algorithms=authjwt.authjwt_algorithm)
            return payload
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid {token_type} Token")

    def verify_expire_token(self, token: str, token_type: str) -> dict:
        payload: dict = self.__decode_token(token, token_type)
        expire = payload.get("expire")
        if expire is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"{token_type} Token missing 'expire' field")

        try:
            expire_time = datetime.fromisoformat(expire)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"Invalid 'expire' format in {token_type} Token")

        if expire_time < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{token_type} Token Expired")
        return payload

    def create_refresh_token(self, schema: UserSchema) -> str:
        token_data: RefreshTokenSchema = RefreshTokenSchema(user_id=schema.user_id)
        token: str = self.__create_token(token_data,
                                         expire=datetime.now(timezone.utc) + timedelta(minutes=authjwt.refresh_expire))
        return  token


    def create_access_token(self, schema:  UserSchema):
        token_data: AccessTokenSchema = AccessTokenSchema(user_id=schema.user_id,
                                                          role=schema.role,
                                                          )
        token: str = self.__create_token(token_data,
                                         expire=datetime.now(timezone.utc) + timedelta(minutes=authjwt.access_expire))
        return  token









