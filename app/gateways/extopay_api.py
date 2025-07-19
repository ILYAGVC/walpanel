from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

import requests
import os

from app.db.engine import get_db
from app.log.logger_config import logger
from app.oprations.payment_settings import payment_setting_query
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

EXTOPAY_CALLBACK_URL = str(os.getenv("EXTOPAY_CALLBACK_URL"))


class ExtopayApi:
    def __init__(self):
        self.base_url = " https://api.digiarvan.org"
        self.headers = {"Content-Type": "application/json"}

    async def make_payment_url(
        self,
        order_id: str,
        amount: int,
        db: Session,
    ) -> Optional[Dict[str, Any]]:
        """
        Returns:
            Dict containing payment URL and details if successful, None if failed
        """
        try:
            key = await payment_setting_query.get_extopay_key(db)
            url = f"{self.base_url}/payment/request?key={key['key']}"
            data = {
                "amount": amount,
                "description": str(order_id),
            }

            response = requests.post(url=url, json=data, headers=self.headers)
            response_data = response.json()
            logger.info(f"Payment API Response: {response_data}")

            if not isinstance(response_data, dict):
                logger.error(f"Invalid response format: {response_data}")
                return None

            if response_data.get("payment_url"):
                return {
                    "link": response_data["payment_url"],
                    "authority": response_data["authority"],
                }
            else:
                logger.error(f"Payment URL generation failed: {response_data}")
                return None

        except Exception as e:
            logger.error(f"Error in make_payment_url: {e}")
            return None

    async def check_payment_status(self, Authority: str) -> Optional[Dict[str, Any]]:
        """
        Check payment status using token
        """
        try:
            key = await payment_setting_query.get_extopay_key()
            url = f"{self.base_url}/verify?key={key['key']}&Authority={Authority}"

            response = requests.get(url=url, headers=self.headers)
            response_data = response.json()
            logger.info(f"Payment status check response: {response_data}")

            if not response_data.get("card_pan"):
                logger.error(f"Payment status check failed. Response: {response_data}")
                return None

            return {
                "result": True,
                "message": response_data["message"],
                "card_pan": response_data["card_pan"],
                "ref_id": response_data["ref_id"],
                "fee": response_data("fee"),
                "shaparak_fee": response_data("shaparak_fee"),
                "order_id": response_data["order_id"],
            }

        except Exception as e:
            logger.error(f"Error in check_payment_status: {e}")
            return None


extopay_api = ExtopayApi()
