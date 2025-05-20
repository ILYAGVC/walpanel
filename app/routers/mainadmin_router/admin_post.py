from fastapi import APIRouter, Depends
from app.schema._input import CreateAdminInput, UpdateAdminInput
from app.schema.output import AdminDisplay
from sqlalchemy.orm import Session
from app.db.engine import get_db
from app.oprations.admin import admin_operations
from app.auth.auth_controller import mainadmin_required

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/create", response_model=AdminDisplay)
def create_admin(
    request: CreateAdminInput,
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    return admin_operations.create_admin(db, request)


@router.post("/edit", response_model=AdminDisplay)
def edit_admin(
    request: UpdateAdminInput,
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    return admin_operations.edit_admin(db, request)
