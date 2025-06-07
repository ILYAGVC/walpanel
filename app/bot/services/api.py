from typing import Optional, Dict, Any

import requests

from app.bot.config import EXTOPAY_CALLBACK_URL
from app.log.logger_config import logger
from app.bot.services.query import payment_gateway_query


class IntermediaryGatewayAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://dgpaneltr.sbs/zirgozar/api"
        self.headers = {"Content-Type": "application/json"}

    async def make_a_payment_url(
        self,
        order_id: str,
        amount: int,
        callback_url: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Returns:
            Dict containing payment URL and details if successful, None if failed
        """
        try:
            url = f"{self.base_url}/index.php"
            data = {
                "key": self.api_key,
                "action": "web_pay",
                "amount": amount,
                "order_id": order_id,
                "callback_url": callback_url,
            }

            response = requests.post(url=url, json=data, headers=self.headers)
            response_data = response.json()
            logger.info(f"Payment API Response: {response_data}")

            if not isinstance(response_data, dict):
                logger.error(f"Invalid response format: {response_data}")
                return None

            if not response_data.get("result"):
                logger.error(f"Payment failed. Response: {response_data}")
                return None

            if response_data.get("result"):
                return {
                    "result": response_data["result"],
                    "code": response_data["code"],
                    "token": response_data["token"],
                    "link": response_data["link"],
                }
            else:
                logger.error(f"Payment URL generation failed: {response_data}")
                return None

        except Exception as e:
            logger.error(f"Error in make_a_payment_url: {e}")
            return None

    async def check_payment_status(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Check payment status using token
        """
        try:
            url = f"{self.base_url}/index.php"
            data = {"key": self.api_key, "action": "web_pay_status", "token": token}

            response = requests.post(url=url, json=data, headers=self.headers)
            response_data = response.json()
            logger.info(f"Payment status check response: {response_data}")

            if not response_data.get("result"):
                logger.error(f"Payment status check failed. Response: {response_data}")
                return None

            return {
                "result": response_data["result"],
                "token": response_data["token"],
                "pay_id": response_data["pay_id"],
                "payer_mobile": response_data.get("payer_mobile"),
                "payer_card": response_data.get("payer_card"),
                "amount": response_data["amount"],
                "status": response_data["status"],
                "order_id": response_data["order_id"],
            }

        except Exception as e:
            logger.error(f"Error in check_payment_status: {e}")
            return None


# Create an instance with your API key
api_key = payment_gateway_query.get_intermediary_gateway_key()
intermediary_api = IntermediaryGatewayAPI(api_key=api_key)
