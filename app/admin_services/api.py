from py3xui import Api
from py3xui.client import Client

import json
import logging

logger = logging.getLogger(__name__)


class PanelAPI:
    def __init__(self, address: str, username: str, password: str):
        self.api = Api(
            host=f"https://{address}",
            username=username,
            password=password,
        )
        try:
            self.api.login()
            logger.info("Logged in successfully ✅")
        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise

    def add_user(self, inb_id, _uuid, subid, email, totalGB, expiryTime, flow):
        try:
            new_client = Client(
                id=_uuid,
                enable=True,
                email=email,
                flow=flow,
                total_gb=totalGB,
                expiry_time=expiryTime,
                sub_id=subid,
                limit_ip=0,
            )
            self.api.client.add(inb_id, [new_client])
            return True
        except Exception as e:
            logger.error(f"Create client failed (inb_id={inb_id}, email={email}): {e}")
            return None

    def show_users(self, inb_id):
        try:
            inb = self.api.inbound.get_by_id(inb_id)
            users = inb.settings.clients
            return users
        except Exception as e:
            logger.error(f"Failed to fetch users: {e}")
            return None

    def get_user(self, email):
        try:
            return self.api.client.get_by_email(email)
        except Exception as e:
            logger.error(f"Get user failed: {e}")
            return None

    def reset_traffic(self, inb_id, email):
        try:
            self.api.client.reset_stats(inb_id, email)
            return True
        except Exception as e:
            logger.error(f"Reset traffic failed: {e}")
            return None

    def update_client(
        self,
        inb_id,
        user_id,
        email,
        totalGB,
        expirTime,
        inboud_flow,
        subid,
    ):
        settings = Client(
            id=user_id,
            inbound_id=inb_id,
            email=email,
            totalGB=totalGB,
            expiryTime=expirTime,
            flow=inboud_flow,
            subId=subid,
            enable=True,
        )
        try:
            self.api.client.update(user_id, settings)
            logger.info(f"Client {email} updated successfully in inbound {inb_id}")
            return True
        except Exception as e:
            logger.error(f"Update client failed (inb_id={inb_id}, uuid={user_id}): {e}")
            return None

    def delete_client(self, inb_id, user_id):
        try:
            return self.api.client.delete(inb_id, user_id)
        except Exception as e:
            logger.error(f"Delete client failed: {e}")
            return None

    def server_status(self):
        try:
            result = self.api.server.get_status()
            return result
        except Exception as e:
            logger.error(f"Server status failed: {e}")
            return None
