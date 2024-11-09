from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.routers.admin.utils import action_add_new_payment, action_get_all_account, action_get_admin_analysis, action_get_transaction_history
from src.schemas.SignInFormSchema import AccountRegisterSchema
from src.routers.account.utils import (action_user_register,
                                       action_login)
from src.lib.jwt_authenication_handler import jwt_validator, jwt_validator_admin
from src.models.account import account
from src.schemas.BodyResponseSchema import BodyResponseSchema
from src.schemas.AddPaymentSchema import AddPaymentSchema

admin_router = APIRouter(prefix="/api/admin", tags=["Admin"])
@admin_router.get("/user", response_model=BodyResponseSchema, dependencies=[Depends(jwt_validator_admin)])
async def get_account_info():
    all_account = await action_get_all_account()
    return {"data" : all_account}


@admin_router.get("/analysis", response_model=BodyResponseSchema, dependencies=[Depends(jwt_validator_admin)])
async def get_status_analysis():
    return {"data" :[await action_get_admin_analysis()]}

@admin_router.get("/transaction", response_model=BodyResponseSchema, dependencies=[Depends(jwt_validator_admin)])
async def get_transaction_history():
    return {"data" :[await action_get_transaction_history()]}

@admin_router.post("/payment", response_model=BodyResponseSchema, 
    dependencies=[Depends(jwt_validator_admin)], status_code=201)
async def add_payment(request_data: AddPaymentSchema):
    return {"data" :[await action_add_new_payment(request_data)]}
    