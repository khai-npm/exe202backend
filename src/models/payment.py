from beanie import Document, Indexed
from datetime import datetime
from fastapi import Form
from pydantic import BaseModel

class payment(Document):
    payment_date : datetime
    payment_ammount : float
    payment_code : str
    status : int = 0
    class Settings:
        name = "system_bill"