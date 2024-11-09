from datetime import datetime
from typing import Annotated

from bson import ObjectId
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.models.account import account
from src.schemas.BodyResponseSchema import BodyResponseSchema
from src.schemas.SignInFormSchema import AccountRegisterSchema
from src.lib.regular_expression import contains_special_character
from src.lib.hash_password import hash_password_util
from src.lib.jwt_authenication_bearer import authenticate_user,create_access_token
from src.models.payment import payment

async def action_user_register(request_data : AccountRegisterSchema):
    try:
        if (request_data.username == "" or
            request_data.password =="" or
            request_data.confirm_password=="" or
            request_data.discord_userid==""):
            raise Exception("Invalid Input: request data's field must not be null!")
        
        if (" " in request_data.username or
            " " in request_data.password or
            " " in request_data.confirm_password or
            " " in request_data.discord_userid):
            raise Exception("Invalid Input: contain space character")
        
        if contains_special_character(request_data.username):
            raise Exception("Invalid Input: username contain special character")

        if await account.find_one(account.username == request_data.username):
            raise Exception("username already exist !")
        
        if request_data.password != request_data.confirm_password:
            raise Exception("password confirmation not matched!")
        
        new_account = account(username=request_data.username,
                                   password=hash_password_util.HashPassword(request_data.password), 
                                   create_date=datetime.now(),
                                   wallet=0,
                                   token_id=[],
                                   discord_user_id=request_data.discord_userid,
                                   payment_info_id=[],
                                   role=1,
                                   status=True
                                   )
        
        await new_account.insert()

        return BodyResponseSchema(data=["account registered successfully !"])
        


    except Exception as e:
        return BodyResponseSchema(success=False, error=str(e))
    


async def action_login(from_data : OAuth2PasswordRequestForm):
    try:
        user_in_db = await account.find_one(account.username == from_data.username)
        if not user_in_db:
            raise Exception("incorrect username or password!")
        
        if user_in_db.status is False:
            raise Exception("inactive account")
        
        user_in_db = user_in_db.model_dump()
        
        if not authenticate_user(user_in_db, from_data.password):
            raise Exception("incorrect username or password!")

        return create_access_token(user_in_db)



    except Exception as e:
        return BodyResponseSchema(success=False, error=str(e))
        
async def action_get_payment_info_by_user(current_user : str):
    user = await account.find_one(account.username == current_user)
    if not user:
        raise HTTPException(detail="user not found", status_code=401)
    
    result : list[payment] = []
    for payment_id in user.payment_info_id:
        get_payment_info = await payment.find_one(payment.id == ObjectId(payment_id))
        result.append(get_payment_info)

    result.reverse()

    return result


