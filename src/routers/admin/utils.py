from fastapi import HTTPException
from src.models.account import account
from src.models.server import server
from src.models.token import token
from src.schemas.GetAdminAccountSchema import GetAdminAccountSchema, GetAdminDataAnalysis

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

    

    