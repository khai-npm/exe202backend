from pydantic import BaseModel

class AddPaymentSchema(BaseModel):
    username : str
    payment_ammount : float
    payment_code : str
    two_factor_master_authenication_code : str