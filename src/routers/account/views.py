from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.SignInFormSchema import AccountRegisterSchema
from src.routers.account.utils import (action_user_register,
                                       action_login)
from src.lib.jwt_authenication_handler import jwt_validator
from src.models.account import account

account_router = APIRouter(prefix="/api/account", tags=["Account"])
@account_router.post("/register")
async def register_account(new_account : AccountRegisterSchema):
    return await action_user_register(new_account)

@account_router.post("/login")
async def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await action_login(form_data)

@account_router.get("/jwt_test", dependencies=[Depends(jwt_validator)])
async def test_jwt():
    try:
        return {"success" : True}
    except Exception as e:
        return {"success" : False, 
                "error" : str(e)}

    

