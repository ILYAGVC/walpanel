from app.log.logger_config import logger
from app.oprations.admin import admin_operations
import requests
import os
import json


class PanelAPI:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {"Accept": "application/json"}
        self.logged_in_panels = set()

    def login(self, address, username, password):
        try:
            url = f"https://{address}/login"
            data = {"username": username, "password": password}

            response = self.session.post(
                url, data=data, headers=self.headers, timeout=30
            )

            if response.status_code == 200:
                self.logged_in_panels = f"{address}|{username}"
                return True
            else:
                logger.error(f"Login failed with status code: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False

    def login_with_out_savekey(self, address, username, password):
        try:
            url = f"https://{address}/login"
            data = {"username": username, "password": password}

            response = self.session.post(
                url, data=data, headers=self.headers, timeout=30
            )
            if response.status_code == 200:
                return True
            else:
                logger.error(
                    f"Login failed without save key status code: {response.status_code}"
                )
                return False
        except Exception as e:
            logger.error(f"Error during login without save key: {e}")
            return False

    def _make_request(self, method, url, **kwargs):
        address = kwargs.pop("address", "")
        username = kwargs.pop("username", "")
        password = kwargs.pop("password", "")
        json_response = kwargs.pop("json_response", False)
        key = f"{address}|{username}"

        kwargs.setdefault("timeout", 30)

        try:
            if key not in self.logged_in_panels:
                if not self.login(address, username, password):
                    return None

            response = method(url, **kwargs)
            if response.status_code == 401:

                logger.warning(f"Session expired for {address}, re-logging in...")
                self._logged_in_panels.discard(key)
                if self.login(address, username, password):
                    response = method(url, **kwargs)

            if response.ok:
                return response.json() if json_response else response
            else:
                logger.warning(f"Request failed with status: {response.status_code}")
                return None

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
                    "security": "auto",
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

    def user_status(self, panel):
        url = f"https://{panel}/panel/inbound/onlines"
        response = self.session.post(url)
        return response.json()

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
