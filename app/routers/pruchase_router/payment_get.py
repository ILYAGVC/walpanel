from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.oprations.payment_settings import payment_setting_query
from app.auth.auth_controller import mainadmin_required

router = APIRouter(prefix="/payment", tags=["Payments"])


@router.get("/get-cardnumber")
async def get_cardnumber(
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    return await payment_setting_query.get_card_number(db)


@router.get("/get-extopay-key")
async def get_extopay_key(
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    return await payment_setting_query.get_extopay_key(db)


@router.get("/get-payment-setting")
async def get_payment_setting(
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    return await payment_setting_query.get_payment_setting(db)


@router.get("/change-card-payment-status")
async def change_card_payment_status(
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    return await payment_setting_query.update_cardpayment_status(db)


@router.get("/change-extopay-payment-status")
async def change_extopay_payment_status(
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    return await payment_setting_query.update_extopay_status(db)
