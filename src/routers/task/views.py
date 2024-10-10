from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.routers.task.utils import action_get_task_by_current_user
from src.lib.jwt_authenication_handler import jwt_validator, get_current_user

task_router = APIRouter(prefix="/api/v2/task", tags=["Task"])

@task_router.get("/current_user")
async def get_task_by_current_user(current_user:str = Depends(get_current_user)):
    return await action_get_task_by_current_user(current_user)
    