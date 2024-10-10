import datetime
from src.models.task import task
from pydantic import BaseModel



class ServerTaskResponseSchema(BaseModel):
    server_id : str
    server_name : str
    tasks : list[task]