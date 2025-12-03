from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from backend.db import crud
from backend.db.engin import get_db
from backend.auth import get_current_admin
from backend.schema.output import AdminOutput, ResponseModel, PanelOutput

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", description="Get dashboard data")
async def read_dashboard_data(
    db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)
):
    if current_admin["role"] == "superadmin":
        all_admins = crud.get_all_admins(db)
        all_panels = crud.get_all_panels(db)
        return ResponseModel(
            success=True,
            message="Data retrieved successfully",
            data={
                "admins": [AdminOutput.from_orm(admin) for admin in all_admins],
                "panels": [PanelOutput.from_orm(panel) for panel in all_panels],
            },
        )

        ...

    if current_admin["role"] == "admin":
        ...
