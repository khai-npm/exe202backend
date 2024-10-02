from beanie import Document, Indexed
from datetime import datetime
from fastapi import Form
from pydantic import BaseModel

class participant(Document):
    server_id: str
    redeem_token : str
    server_owner : str
    server_name : str
    tasks : list[str]
    class Settings:
        name = "participant"

