from py3xui import Api
from py3xui.client import Client

import json
import logging

logger = logging.getLogger(__name__)


class PanelAPI:
    _api_instance = None
    _login_status = False

    def __init__(self, address: str, username: str, password: str):
        self.address = address
        self.username = username
        self.password = password
        self._get_api_instance()

    def _get_api_instance(self):
        """Get or create API instance"""
        needs_login = PanelAPI._api_instance is None or not PanelAPI._login_status

        if not needs_login:
            try:
                login_check = PanelAPI._api_instance.server.get_status()
                if not hasattr(login_check, "xray"):
                    logger.info("Session expired, re-logging in...")
                    needs_login = True
            except Exception as e:
                logger.warning(f"Session check failed: {e}")
                needs_login = True

        if needs_login:
            PanelAPI._api_instance = Api(
                host=f"https://{self.address}",
                username=self.username,
                password=self.password,
            )
            PanelAPI._api_instance.login()
            PanelAPI._login_status = True
            logger.info("Logged in successfully!")

        self.api = PanelAPI._api_instance

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
            all_inbounds = self.api.inbound.get_list()
            inb = next((i for i in all_inbounds if i.id == inb_id), None)

            if not inb:
                logger.error(f"Inbound with ID {inb_id} not found.")
                return None
            if not inb.client_stats:
                logger.warning(
                    f"client_stats is missing for inbound {inb_id}. Returning users without traffic stats."
                )
                return inb.settings.clients

            stats_map = {stat.email: stat for stat in inb.client_stats}
            clients_with_config = inb.settings.clients
            for client_config in clients_with_config:
                client_stat = stats_map.get(client_config.email)
                if client_stat:
                    client_config.up = client_stat.up
                    client_config.down = client_stat.down
                    client_config.enable = client_stat.enable
            return clients_with_config
        except Exception as e:
            logger.error(f"Failed to fetch users for inbound {inb_id}: {e}")
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

    def online_users(self) -> list:
        try:
            return self.api.client.online()
        except Exception as e:
            logger.error(f"Online users fetch failed: {e}")
            return None
