from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import datetime
from app.db.engine import get_db
from sqlalchemy.orm import Session

import time
import random

from app.auth.auth_controller import get_current_user
from app.gateways.extopay_api import extopay_api
from app.oprations.admin import admin_operations
from app.log.logger_config import logger

router = APIRouter(prefix="/payment", tags=["payment"])

waiting_payments = {}

@router.get("/Extopay/")
async def payment_request(
    db: Session = Depends(get_db),
    amount: int = Query(..., description="the plan price"),
    plan_id: int = Query(..., description="plan id"),
    username: str = Depends(get_current_user)
):
    try:
        order_time = datetime.now().strftime('%Y%m%d')
        rand_num = random.randint(1,85)
        order_id = f"{username['username']}_{plan_id}_{order_time}_{rand_num}"
        logger.info(
            f"Received payment request: amount={amount}, order_id={order_id}"
        )
        res = await extopay_api.make_payment_url(order_id, amount, db)
        waiting_payments[res["authority"]] = order_id
        return {
            "status": True,
            "link": res["link"],
            "authority": res["authority"]
            }
    
    except HTTPException as e:
        logger.error(f"Error during payment request: {e}")
        raise HTTPException(status_code=400, detail="Payment request failed")


@router.get("/callback/")
async def payment_callback(
    Authority: str = Query(..., description="Authority"),
    Status: str = Query(..., description="Payment result (OK or NOK)"),
    db: Session = Depends(get_db),
):
    try:
        logger.info(
            f"Received payment callback: Authority={Authority}, status={Status}"
        )

        if Status == "OK" and Authority in waiting_payments:
            payment_status = await extopay_api.check_payment_status(Authority, db)
            logger.info(f"Payment status from gateway: {payment_status}")

            if not payment_status:
                logger.error(f"Failed to get payment status for Authority: {Authority}")
                raise HTTPException(
                    status_code=400, detail="Failed to verify payment status"
                )

            # Verify payment is paid
            if not payment_status["result"]:
                logger.error(f"Payment verification failed. Status: {payment_status}")
                raise HTTPException(
                    status_code=400, detail="Payment verification failed"
                )
            
            order_id = waiting_payments[Authority]
            username, plan_id, timestamp, rand_num = (order_id.split("_"))
            # Convert string timestamp to date object
            purchase_date = datetime.strptime(timestamp, "%Y%m%d").date()
            
            result = await admin_operations.aproval_payment_(db, username, plan_id)
            if result:
                waiting_payments.pop(Authority)
                logger.info(f"Payment successful: username={username}, plan_id={plan_id}")
                return {"status": True, "message": "Payment completed successfully."}
            
        else:  # result is NOK
            if Authority in waiting_payments:
                order_id = waiting_payments[Authority]
                waiting_payments.pop(Authority)
                logger.info(f"Payment was cancelled or failed for order_id: {order_id}")
                return {"status": False, "message": "Payment was cancelled or failed."}
            else:
                logger.info(f"Payment was cancelled or failed for authority: {Authority}")
                return {"status": False, "message": "Payment was cancelled or failed."}


    except Exception as e:
        logger.error(f"Error processing payment callback: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
