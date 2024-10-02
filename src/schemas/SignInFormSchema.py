from typing import Any, List
from pydantic import BaseModel


class AccountRegisterSchema(BaseModel):
    username : str
    password : str
    confirm_password : str
    discord_userid : str