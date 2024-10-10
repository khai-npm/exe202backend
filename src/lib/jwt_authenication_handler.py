import time
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from src.models.account import account

import os
from dotenv import load_dotenv

# DB_CONNECTION_STRING = app_settings.MONGODB_URL
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


if not JWT_ALGORITHM or not JWT_SECRET:
    raise ValueError("JWT authorizer not found ! check .ENV for more info !")
print("using algo :" + JWT_ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/account/login")


async def jwt_validator(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload['is_refresh_token'] is True:
             raise credentials_exception
        if payload['role'] is None:
             raise credentials_exception
        username: str = payload.get("username")
        expire_time: float = payload.get("exp")
        if username is None or expire_time <= time.time():
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = await account.find_one({"username": username})
    if user is None:
        raise credentials_exception
    


async def jwt_validator_admin(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload['is_refresh_token'] is True:
             raise credentials_exception
        if payload['role'] != 2:
             raise credentials_exception
        username: str = payload.get("username")
        expire_time: float = payload.get("exp")
        if username is None or expire_time <= time.time():
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = await account.find_one({"username": username})
    if user is None:
        raise credentials_exception

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        acc_info = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = acc_info.get("username")
        return username