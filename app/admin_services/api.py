from app.log.logger_config import logger
from app.oprations.admin import admin_operations
import requests
import os
import json


class PanelAPI:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {"Accept": "application/json"}
        self._current_panel = None

    def login(self, address, username, password):
        try:
            url = f"https://{address}/login"
            data = {"username": username, "password": password}

            response = self.session.post(
                url, data=data, headers=self.headers, timeout=30
            )

            if response.status_code == 200:
                self._current_panel = (address, username, password)
                return True
            else:
                logger.error(f"Login failed with status code: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False

    def _make_request(self, method, url, **kwargs):
        address = kwargs.pop("address", "")
        username = kwargs.pop("username", "")
        password = kwargs.pop("password", "")
        json_response = kwargs.pop("json_response", False)

        kwargs.setdefault("timeout", 30)

        try:
            if not self.login(address, username, password):
                logger.error(f"Login failed for {address}")
                return None

            response = method(url, **kwargs)
            if response.ok and json_response:
                return response.json()
            return response

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error in request: {e}")
            return None

    def add_user(
        self,
        panel,
        username,
        password,
        inb_id,
        _uuid,
        subid,
        email,
        totalGB,
        expiryTime,
    ):

        url = f"https://{panel}/panel/inbound/addClient"
        settings = {
            "clients": [
                {
                    "id": _uuid,
                    "enable": True,
                    "flow": "",
                    "email": email,
                    "imitIp": 0,
                    "totalGB": totalGB,
                    "expiryTime": expiryTime,
                    "tgId": "",
                    "subId": subid,
                    "reset": "",
                }
            ]
        }
        data = {"id": inb_id, "settings": json.dumps(settings)}
        response = self._make_request(
            self.session.post,
            url,
            json=data,
            address=panel,
            username=username,
            password=password,
        )
        return response.json()

    def show_users(self, panel, username, password, inb_id):
        url = f"https://{panel}/panel/api/inbounds/get/{inb_id}"
        response = self._make_request(
            self.session.get,
            url,
            address=panel,
            username=username,
            password=password,
        )
        if response and response.status_code == 200:
            return response.json()
        else:
            return {
                "error": "Failed to fetch users",
                "status_code": response.status_code if response else "no response",
            }

    def user_obj(self, panel, email):
        url = f"https://{panel}/panel/api/inbounds/getClientTraffics/{email}"
        response = self.session.get(url)
        return response.json()

    def reset_traffic(self, panel, username, password, inb_id, email):
        url = f"https://{panel}/panel/api/inbounds/{inb_id}/resetClientTraffic/{email}"
        return self._make_request(
            self.session.post,
            url,
            address=panel,
            username=username,
            password=password,
        )

    def update_client(self, panel, username, password, inb_id, user_id, updated_client):
        url = f"https://{panel}/panel/api/inbounds/updateClient/{user_id}"
        settings = {"clients": [updated_client]}
        data = {"id": inb_id, "settings": json.dumps(settings)}
        return self._make_request(
            self.session.post,
            url,
            json=data,
            address=panel,
            username=username,
            password=password,
        )

    def delete_client(self, panel, username, password, inb_id, user_id):
        url = f"https://{panel}/panel/api/inbounds/{inb_id}/delClient/{user_id}"
        return self._make_request(
            self.session.post,
            url,
            address=panel,
            username=username,
            password=password,
        )

    async def server_status(self, panel, username, password):
        url = f"https://{panel}/server/status"
        response = self._make_request(
            self.session.post,
            url,
            address=panel,
            username=username,
            password=password,
            json_response=True,
        )
        return response


panels_api = PanelAPI()
