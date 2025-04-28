from fastapi import APIRouter, Depends
from app.auth.auth_controller import get_current_user
from app.db.engine import get_db
from app.oprations.admin import admin_operations
from sqlalchemy.orm import Session
from app.admin_services.task import admin_task
from app.schema._input import CreateUserInput, UpdateUserInput


router = APIRouter(prefix="/admin", tags=["Admin dashboard"])


@router.post("/CreateClient")
async def create_suer(
    request: CreateUserInput,
    db: Session = Depends(get_db),
    username: dict = Depends(get_current_user),
):
    if admin_operations.pre_opration_check(db, username["username"]):
        return admin_task.create_user(db, username["username"], request)


@router.post("/DeleteClient/{user_id}")
async def delete_client(
    user_id: str,
    db: Session = Depends(get_db),
    username: dict = Depends(get_current_user),
):
    return admin_task.delete_client(db, username["username"], user_id)


@router.post("/UpdateClient/{user_id}")
async def update_client(
    user_id: str,
    request: UpdateUserInput,
    db: Session = Depends(get_db),
    username: dict = Depends(get_current_user),
):
    if admin_operations.pre_opration_check(db, username["username"]):
        return admin_task.update_client(db, username["username"], user_id, request)


@router.post("/ResetTraffic/{email}")
async def reset_traffic(
    email: str,
    db: Session = Depends(get_db),
    username: dict = Depends(get_current_user),
):
    if admin_operations.pre_opration_check(db, username["username"]):
        return admin_task.reset_client_traffic(db, username["username"], email)
