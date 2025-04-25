from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.engine import get_db
from app.oprations.panel import panel_operations
from app.schema.output import PanelsListOutput
from app.auth.auth_controller import mainadmin_required

router = APIRouter(prefix="/panel", tags=["Panel"])


@router.get("/all", response_model=PanelsListOutput)
def get_all_panels(
    db: Session = Depends(get_db), username: str = Depends(mainadmin_required)
):
    panels = panel_operations.get_panels(db)
    return {"panels": panels}


@router.get("/delete/{id}")
def delete_panel(
    id: int, db: Session = Depends(get_db), username: str = Depends(mainadmin_required)
):
    return panel_operations.delete_panel(db, id)


@router.get("/statuses")
async def get_panel_status(
    db: Session = Depends(get_db), username: str = Depends(mainadmin_required)
):
    return await panel_operations.get_panel_status(db)
