from src.models.account import account
from src.models.task import task
from src.models.server import server
from src.schemas.BodyResponseSchema import BodyResponseSchema
from src.schemas.ServerTaskResponseSchema import ServerTaskResponseSchema


from fastapi import HTTPException


async def action_get_task_by_current_user(current_user : str):
    try:
        user = await account.find_one(account.username == current_user)
        if not user:
            raise HTTPException(detail="not found user", status_code=404)
        
        user_discord = user.discord_user_id
        target_server_list = await server.find_many(server.server_owner == user_discord).to_list()

        fdata : list[ServerTaskResponseSchema] = []
        for i in target_server_list:

            task_list = await task.find_many(task.server_id == i.server_id).to_list()
            new_data = ServerTaskResponseSchema(
                server_id=i.server_id,
                server_name=i.server_name,
                tasks=task_list
            ) 

            fdata.append(new_data)


        return BodyResponseSchema(data=fdata)

        
        
    except Exception as e:
        return BodyResponseSchema(success=False, error=str(e))