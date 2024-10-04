from beanie import Document, Indexed
from datetime import datetime
from fastapi import Form
from pydantic import BaseModel

class task(Document):
    add_by : str
    server_id : str
    task_title : str
    task_desc : str
    start_date : datetime
    end_date : datetime
    participants : list[str]
    success : bool
    class Settings:
        name = "task"