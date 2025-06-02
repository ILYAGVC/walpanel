from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.oprations.panel import panel_operations
from app.schema._input import CreateNews
from app.db.engine import get_db
from app.auth.auth_controller import mainadmin_required

router = APIRouter(prefix="/news", tags=["News"])


@router.post("/create")
async def create_news(
    request: CreateNews,
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    create = await panel_operations.create_news(db, request)
    return create
