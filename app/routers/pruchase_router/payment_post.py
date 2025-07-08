from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

from app.log.logger_config import logger
from app.schema._input import AddNewCardNumber, AddNewExtopayKey
from app.db.engine import get_db
from app.oprations.payment_settings import payment_setting_query
from app.auth.auth_controller import mainadmin_required, get_current_user
import time

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


@router.post("/upload-receipt-image/{plan_id}")
async def upload_receipt_image(
    plan_id: int,
    file: UploadFile = File(media_type="image/*"),
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user),
):
    image = file.file.read()
    if not image:
        return {
            "status": False,
            "message": "No image uploaded.",
        }
    try:
        now = time.strftime("%Y-%m-%d-%H-%M-%S")
        image_path = f"data/receipts/{username['username']}_{now}_{plan_id}.jpg"
        with open(image_path, "wb") as f:
            f.write(image)
        return {
            "status": True,
            "message": "Receipt image uploaded successfully.",
        }
    except Exception as e:
        logger.error(f"Error uploading receipt image: {e}")
        return {
            "status": False,
            "message": f"Error uploading receipt image",
        }