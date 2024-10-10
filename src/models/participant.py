from beanie import Document, Indexed
from datetime import datetime
from fastapi import Form
from pydantic import BaseModel

class participant(Document):
    discord_user_name : str
    class Settings:
        name = "participant"

