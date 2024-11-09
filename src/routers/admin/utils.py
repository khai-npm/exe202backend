from datetime import datetime
from fastapi import HTTPException
from src.schemas.AddPaymentSchema import AddPaymentSchema
from src.models.account import account
from src.models.server import server
from src.models.token import token
from src.schemas.GetAdminAccountSchema import GetAdminAccountSchema, GetAdminDataAnalysis
from src.models.payment import payment
from src.models.account import account
from dotenv import load_dotenv
import os
load_dotenv()



PAYMENT_SECRET_CODE = os.getenv("PAYMENT_SECRET_CODE")

async def action_get_all_account():
    all_account =  await account.find().project(GetAdminAccountSchema).to_list()

    if len(all_account)==0:
        raise HTTPException(detail="not found account", status_code=404)
    

    return all_account


async def action_get_admin_analysis():
    total_user = await account.find_all().to_list()
    total_user_num = len(total_user)
    active_user_num : int = 0
    for i in total_user:
        detect_active = await server.find_one(server.server_owner == i.discord_user_id)
        if detect_active:
            active_user_num = active_user_num + 1
    premium_token = await token.find_all().to_list()
    premium_user_num = len(premium_token)

    percentage_premium_user = (premium_user_num/total_user_num)*100
    percentage_user_rate = (active_user_num/total_user_num)*100

    return GetAdminDataAnalysis(active_user=active_user_num,
                                total_user=total_user_num,
                                premium_user=premium_user_num,
                                percentage_user_rate=percentage_user_rate,
                                percentage_premium_user=percentage_premium_user)


async def action_add_new_payment(request_data : AddPaymentSchema):
    print(PAYMENT_SECRET_CODE)
    if request_data.two_factor_master_authenication_code != PAYMENT_SECRET_CODE:
        raise HTTPException(detail="2factor authen failed" ,status_code=401)

    if (request_data.username is None 
        or request_data.payment_code is None
        or request_data.payment_ammount < 0):
        raise HTTPException(detail="wrong input" ,status_code=400)
    
    if await payment.find_one(payment.payment_code==request_data.payment_code):
        raise HTTPException(detail="payment code already inputted !" ,status_code=400)

     
    target_account = await account.find_one(account.username == request_data.username)
    if target_account is None:
        raise HTTPException(detail="user not found" ,status_code=404)
    
    new_payment_info = payment(
        status=1,
        payment_date = datetime.now(),
        payment_ammount = request_data.payment_ammount,
        payment_code= request_data.payment_code,
        username= request_data.username
    )

    await new_payment_info.insert()
    await new_payment_info.save()

    target_account.payment_info_id.append(str(new_payment_info.id))
    target_account.wallet = target_account.wallet + request_data.payment_ammount
    await target_account.save()



async def action_get_transaction_history():
    return await payment.find_all().sort(-payment.payment_date).to_list()