from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.schema._input import AddNewCardNumber, AddNewExtopayKey
from app.db.models import CardNumber, PaymentGatewaykeys
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


payment_setting_query = PaymentSettings()
