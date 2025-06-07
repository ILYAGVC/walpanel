from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime


from app.bot.handlers.payment.Intermediary_gateway import payment_filed, payment_is_made
from app.bot.services.api import intermediary_api
from app.log.logger_config import logger

router = APIRouter(prefix="/payment", tags=["payment"])


@router.get("/callback/")
async def payment_callback(
    token: str = Query(..., description="Payment token from gateway"),
    result: str = Query(..., description="Payment result (OK or NOK)"),
    order_id: str = Query(..., description="Order ID from our system"),
):
    try:
        logger.info(
            f"Received payment callback: token={token}, result={result}, order_id={order_id}"
        )

        _, amount, bot_language, plan_id, chat_id, timestamp, randomint = (
            order_id.split("_")
        )
        # Convert string timestamp to date object
        purchase_date = datetime.strptime(timestamp, "%Y%m%d").date()

        if result == "OK":
            payment_status = await intermediary_api.check_payment_status(token)
            logger.info(f"Payment status from gateway: {payment_status}")

            if not payment_status:
                logger.error(f"Failed to get payment status for token: {token}")
                raise HTTPException(
                    status_code=400, detail="Failed to verify payment status"
                )

            # Verify payment is paid
            if not payment_status["result"]:
                logger.error(f"Payment verification failed. Status: {payment_status}")

                await payment_filed(
                    int(amount),
                    str(bot_language),
                    int(plan_id),
                    int(chat_id),
                    str(order_id),
                    timestamp=purchase_date,
                )

                return {
                    "status": "failed",
                    "message": "Payment is not completed yet",
                    "payment_status": payment_status.get("status"),
                    "order_id": order_id,
                }

            # Notify user of successful payment
            await payment_is_made(
                int(amount),
                str(bot_language),
                int(plan_id),
                int(chat_id),
                str(order_id),
                timestamp=purchase_date,
            )

            return {
                "status": "success",
                "message": "Payment verified and processed successfully",
                "payment_details": payment_status,
            }

        else:  # result is NOK
            logger.info(f"Payment was cancelled or failed for order_id: {order_id}")
            await payment_filed(
                int(amount),
                str(bot_language),
                int(plan_id),
                int(chat_id),
                str(order_id),
                timestamp=purchase_date,
            )
            return {
                "status": "cancelled",
                "message": "Payment was cancelled or failed",
                "order_id": order_id,
            }

    except Exception as e:
        logger.error(f"Error processing payment callback: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
