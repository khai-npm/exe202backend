from datetime import datetime
from beanie import init_beanie

from src.lib.hash_password import hash_password_util



async def event_01_init_db():
    import os

    from src.models.account import account
    from src.models.participant import participant
    from src.models.payment import payment
    from src.models.server import server
    from src.models.task import task
    from src.models.token import token
    from motor.motor_asyncio import AsyncIOMotorClient
    from src.database.get_db_instance import connection_string

    if not connection_string:
        raise ValueError("connection string not found. check .ENV is exist or not! ")
    print("Connected Database set: " + connection_string)
    db_instance = AsyncIOMotorClient(connection_string)
    await init_beanie(
        database=db_instance["exe_bot"], document_models=[account, participant, payment,
                                                         server, task, token ]
    )
    if await account.count() == 0:
        new_account = account(username="admin",
                                password=hash_password_util.HashPassword("1"), 
                                create_date=datetime.now(), 
                                wallet=0,
                                token_id= [""],
                                discord_user_id="",
                                payment_info_id=[""],
                                role = 2,
                                status=True
                                )
        await new_account.insert()
        print("insert new admin account")


events = [v for k, v in locals().items() if k.startswith("event_")]