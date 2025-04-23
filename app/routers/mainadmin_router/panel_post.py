from fastapi import APIRouter, Depends
from app.schema._input import CreatePanelInput
from app.schema.output import PanelDisplay
from sqlalchemy.orm import Session
from app.db.engine import get_db
from app.oprations.panel import panel_operations
from app.auth.auth_controller import mainadmin_required

router = APIRouter(prefix="/panel", tags=["Panel"])


# create panel
@router.post("/create", response_model=PanelDisplay)
def create_panel_api(
    request: CreatePanelInput,
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    return panel_operations.create_panel(db, request)


# edit panel
@router.post("/edit/{id}", response_model=PanelDisplay)
def edit_panel(
    id: int,
    request: CreatePanelInput,
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    return panel_operations.edit_panel(db, request, id)
