from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

from app.schema._input import AddNewCardNumber, AddNewExtopayKey
from app.db.engine import get_db
from app.oprations.payment_settings import payment_setting_query
from app.auth.auth_controller import mainadmin_required

router = APIRouter(prefix="/payment", tags=["Payments"])


@router.post("/add-cardnumber")
async def add_cardnumber(
    request: AddNewCardNumber,
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    return await payment_setting_query.add_or_change_card_number(db, request)


@router.post("/add-extopay-key")
async def add_extopay_key(
    request: AddNewExtopayKey,
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    return await payment_setting_query.add_or_change_extopay_key(db, request)
