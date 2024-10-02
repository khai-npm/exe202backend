from beanie import Document, Indexed
from datetime import datetime
from fastapi import Form
from pydantic import BaseModel

class account(Document):
    username : str
    password : str
    create_date : datetime
    wallet : float
    token_id : list[str]
    role : int
    discord_user_id : str
    payment_info_id : list[str]
    class Settings:
        name = "account"




