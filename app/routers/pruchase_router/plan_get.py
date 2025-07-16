from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from sqlalchemy.orm import Session
from app.db.engine import get_db
from app.oprations.purchase_plan import plans_query
from app.auth.auth_controller import mainadmin_required

router = APIRouter(prefix="/plan", tags=["Purchase plan"])


@router.get("/all")
async def get_all_pruchase_plan(db: Session = Depends(get_db)):
    plans = await plans_query.get_plans(db)
    return plans


@router.get("/delete/{id}")
async def delete_a_plan(
    id: int, db: Session = Depends(get_db), username: str = Depends(mainadmin_required)
):
    return await plans_query.delete_plan(db, id)


@router.get("{id}")
async def get_plan_by_id(
    id: int,
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    return await plans_query.get_a_plan_by_id(db, id)
