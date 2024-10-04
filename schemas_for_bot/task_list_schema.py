from pydantic import BaseModel

class task_list_schema(BaseModel):
    task_id : str
    task_title : str