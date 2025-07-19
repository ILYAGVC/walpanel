from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.engine import get_db
from app.oprations.admin import admin_operations
from app.schema.output import AdminsListOutout
from app.auth.auth_controller import mainadmin_required

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/all", response_model=AdminsListOutout)
async def get_all_admins(
    db: Session = Depends(get_db), username: str = Depends(mainadmin_required)
):
    admins = await admin_operations.get_all_admins(db)
    return {"admins": admins}


@router.get("/delete")
def delete_admin(
    id: int, db: Session = Depends(get_db), username: str = Depends(mainadmin_required)
):
    return admin_operations.delete_admin(db, id)
