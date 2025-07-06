from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.schema._input import AddNewCardNumber, AddNewExtopayKey
from app.db.models import CardNumber, PaymentGatewaykeys, Setting
from app.log.logger_config import logger


class PaymentSettings:

    async def get_card_number(self, db: Session):
        try:
            card = db.query(CardNumber).first()
            if not card:
                return {
                    "status": False,
                    "message": "Card number not found.",
                }
            return {
                "status": True,
                "card": card.number,
            }
        except Exception as e:
            logger.error(f"Error in get card number from database: {e}")
            return {
                "status": False,
                "message": f"Error in get card number from database.",
            }

    async def add_or_change_card_number(self, db: Session, request: AddNewCardNumber):
        try:
            card = db.query(CardNumber).first()
            if not card:
                card.number = request.card
                db.commit()
                return {
                    "status": True,
                    "message": "Your new card number has been registered.",
                }
            else:
                card.number = request.card
                db.commit()
                return {
                    "status": True,
                    "message": "Your card number has been updated.",
                }
        except Exception as e:
            logger.error(f"Error in add card number in database: {e}")
            return {
                "status": False,
                "message": f"Error in add card number in database.",
            }

    async def get_extopay_key(self, db: Session):
        try:
            key = db.query(PaymentGatewaykeys).first()
            if not key:
                return {
                    "status": False,
                    "message": "Extopay key not found.",
                }
            return {
                "status": True,
                "key": key.Intermediary_gateway_key,
            }
        except Exception as e:
            logger.error(f"Error in get extopay key from database: {e}")
            return {
                "status": False,
                "message": f"Error in get extopay key from database.",
            }

    async def add_or_change_extopay_key(self, db: Session, request: AddNewExtopayKey):
        try:
            key = db.query(PaymentGatewaykeys).first()
            if not key:
                key = PaymentGatewaykeys(Intermediary_gateway_key=request.key)
                db.add(key)
                db.commit()
                return {
                    "status": True,
                    "message": "Your new Extopay key has been registered.",
                }
            else:
                key.Intermediary_gateway_key = request.key
                db.commit()
                return {
                    "status": True,
                    "message": "Your Extopay key has been updated.",
                }

        except Exception as e:
            logger.error(f"Error in add extopay key in database: {e}")
            return {
                "status": False,
                "message": f"Error in add extopay key in database.",
            }

    async def get_payment_setting(self, db: Session):
        try:
            setting = db.query(Setting).first()
            if not setting:
                return {
                    "status": False,
                    "message": "Payment settings not found.",
                }
            return {
                "status": True,
                "settings": {
                    "card_number": setting.card_payment_enabled,
                    "extopay_key": setting.Intermediary_payment_gateway,
                },
            }
        except Exception as e:
            logger.error(f"Error in get payment settings from database: {e}")
            return {
                "status": False,
                "message": f"Error in get payment settings from database.",
            }

    async def update_cardpayment_status(self, db: Session):
        try:
            setting = db.query(Setting).first()
            setting.card_payment_enabled = not setting.card_payment_enabled
            db.commit()
            return {
                "status": True,
                "message": "Card payment status updated successfully.",
            }
        except Exception as e:
            logger.error(f"Error in update card payment status: {e}")
            return {
                "status": False,
                "message": f"Error in update card payment status.",
            }

    async def update_extopay_status(self, db: Session):
        try:
            setting = db.query(Setting).first()
            setting.Intermediary_payment_gateway = (
                not setting.Intermediary_payment_gateway
            )
            db.commit()
            return {
                "status": True,
                "message": "Extopay payment status updated successfully.",
            }
        except Exception as e:
            logger.error(f"Error in update extopay payment status: {e}")
            return {
                "status": False,
                "message": f"Error in update extopay payment status.",
            }


payment_setting_query = PaymentSettings()
