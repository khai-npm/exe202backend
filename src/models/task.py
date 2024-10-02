from beanie import Document, Indexed
from datetime import datetime
from fastapi import Form
from pydantic import BaseModel

class task(Document):
    task_title : str
    task_desc : str
    start_date : datetime
    end_date : datetime
    participants : list[str]
    class Settings:
        name = "task"