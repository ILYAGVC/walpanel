from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.oprations.panel import panel_operations
from app.schema._input import CreateNews
from app.db.engine import get_db
from app.auth.auth_controller import mainadmin_required

router = APIRouter(prefix="/news", tags=["News"])


@router.get("/all")
async def get_all_news(
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    all_news = await panel_operations.get_news(db)
    return all_news


@router.get("/delete/{id}")
async def delete_news(
    id: int, db: Session = Depends(get_db), username: str = Depends(mainadmin_required)
):

    delete_news = await panel_operations.delete_news(db, id)
    return delete_news
