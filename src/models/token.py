from beanie import Document, Indexed
from datetime import datetime
from fastapi import Form
from pydantic import BaseModel

class token(Document):
        server_id : list[str]
        token : str
        # redeem_date : datetime
        # end_date : datetime
        active : bool
        class Settings:
                name = "token"
