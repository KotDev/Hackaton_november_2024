from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import ValidationError

from authorization.schemas import RegisterSchema, LoginSchema, UserSchema, JWTSchema
from authorization.logic.autorization_logic import AUThLogic, JWTLogic
from authorization.managers.managers import UserManager
from database import redis_client

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
user_manager = UserManager()
auth_logic = AUThLogic()
jwt_logic = JWTLogic()

@auth_router.post("/register", response_model=JWTSchema)
async def register(schema: RegisterSchema) -> JWTSchema:
    try:
        user = await user_manager.get_user(user_id=None, email=schema.email)
        user = user.fetchone()
        if not user:
            pw_hash = auth_logic.password_hash(schema.password)
            user = await user_manager.add_user(schema, pw_hash)
            user_schema = UserSchema(user_id=user.user_id, role=user.role)
            access = jwt_logic.create_access_token(schema=user_schema)
            refresh = jwt_logic.create_refresh_token(schema=user_schema)
            return JWTSchema(access_token=access, refresh_token=refresh)
    except ValidationError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@auth_router.post("/login")
async def login(schema: LoginSchema) -> JWTSchema:
    user = await user_manager.get_user(user_id=None, email=schema.email)
    if not user:
        raise HTTPException(status_code=409, detail="User is not found")
    user = user.scalars().first()
    if auth_logic.verify(schema.password, str(user.password)):
        user_schema = UserSchema(user_id=user.user_id, role=user.role)
        access = jwt_logic.create_access_token(schema=user_schema)
        refresh = jwt_logic.create_refresh_token(schema=user_schema)
        return JWTSchema(access_token=access, refresh_token=refresh)
    else:
        raise HTTPException(status_code=401, detail="Email or Password on invalid")

@auth_router.post("/logout")
async def logout(request: Request, user: UserSchema = Depends(AUThLogic.get_user)):
    refresh_token = request.headers.get("Refresh-Token")
    redis_client.setex(refresh_token, timedelta(days=15), user.user_id)
    return {"detail": "User logged out successfully"}

@auth_router.get("/me")
async def get_me(user: UserSchema = Depends(AUThLogic.get_user)):
    print(user.user_id, print(user.role))