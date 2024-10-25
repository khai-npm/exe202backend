from datetime import datetime
from pydantic import BaseModel

class GetAdminAccountSchema(BaseModel):
    username : str
    create_date : datetime
    wallet : float
    token_id : list[str]
    role : int
    discord_user_id : str
    payment_info_id : list[str]
    status : bool

class GetAdminDataAnalysis(BaseModel):
    active_user : int
    total_user : int
    premium_user : int
    percentage_premium_user : float
    percentage_user_rate : float
    