from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.engine import get_db
from app.oprations.payment_settings import payment_setting_query
from app.oprations.admin import admin_operations
from app.auth.auth_controller import mainadmin_required, get_current_user
from app.oprations.utility import purchase_hisory

import os


router = APIRouter(prefix="/payment", tags=["Payments"])


@router.get("/get-cardnumber")
async def get_cardnumber(
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user),
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
    username: str = Depends(get_current_user),
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


@router.get("/get-receipt-image")
async def get_receipt_image(
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    images_path = "data/receipts/"
    files = os.listdir(images_path)

    image_urls = [f"/data/receipts/{file}" for file in files if file.lower().endswith(('.jpg'))]

    return {"images": image_urls}


@router.get("/delete-receipt-image/{image_name}")
async def delete_receipt_image(
    image_name: str,
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    images_path = "data/receipts/"

    file_path = os.path.join(images_path, image_name)
    dealer_name, timestamp, plan_id, price, _ = image_name.split('_')
    purchase_date = datetime.strptime(timestamp, "%Y-%m-%d-%H-%M-%S").date()
    await purchase_hisory(db, price, purchase_date, dealer_name, "not-done")

    if os.path.exists(file_path):
        os.remove(file_path)
        return {
            "status": True,
            "message": "Image deleted successfully"}
    else:
        return {
            "status": False,
            "message": "Image not found"
        }
    
@router.get("/aproval-payment/{image_name}")
async def aproval_payment(
    image_name: str,
    db: Session = Depends(get_db),
    username: str = Depends(mainadmin_required),
):
    '''
    this function is aproval payment with receipt image
    '''
    dealer_name, timestamp, plan_id, price, _ = image_name.split('_')
    purchase_date = datetime.strptime(timestamp, "%Y-%m-%d-%H-%M-%S").date()

    update_dealer = await admin_operations.aproval_payment_(db, dealer_name, plan_id, price, purchase_date)
    if update_dealer:
        images_path = "data/receipts/"

        file_path = os.path.join(images_path, image_name)
        os.remove(file_path)
        
        return {
            "status": True,
            "message": "Payment approved successfully"
        }
    else:
        return {
            "status": False,
            "message": "Payment not approved"
        }
