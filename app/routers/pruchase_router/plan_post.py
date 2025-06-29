from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schema._input import CreatePlan, Edit_Plan
from sqlalchemy.orm import Session
from app.db.engine import get_db
from app.oprations.purchase_plan import plans_query
from app.auth.auth_controller import mainadmin_required

router = APIRouter(prefix="/plan", tags=["Purchase plan"])


@router.post("/add")
async def add_new_plan(
    request: CreatePlan,
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    return await plans_query.add_plan(db, request)


@router.post("/edit")
async def edit_plan(
    request: Edit_Plan,
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    return plans_query.edit_plan(db, request)
