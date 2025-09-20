import requests
import logging
import json

logger = logging.getLogger(__name__)


class PanelAPI:
    _session = None
    _login_status = False

    def __init__(self, url: str, username: str, password: str):
        self.url = f"https://{url}"
        self.username = username
        self.password = password
        self._get_session()

    def _get_session(self):
        """Get or create a logged-in session"""
        if PanelAPI._session is None or not PanelAPI._login_status:
            session = requests.Session()
            try:
                response = session.post(
                    f"{self.url}/login",
                    json={"username": self.username, "password": self.password},
                    timeout=10,
                )

                if (
                    response.status_code == 200
                    and response.json().get("success") == True
                ):
                    PanelAPI._session = session
                    PanelAPI._login_status = True
                    logger.info(f"Logged in successfully! | url: {self.url}")
                else:
                    logger.error(f"Login failed: {response.text}")
                    raise Exception("Login failed")
            except requests.RequestException as e:
                logger.error(f"Login failed: {e}")
                raise
        self.session = PanelAPI._session

    def get_status(self) -> bool:
        data = self.session.get(f"{self.url}/panel/api/server/status").json()
        return bool(data.get("obj", {}).get("cpu"))

    def login_test(self) -> bool:
        try:
            response = self.session.post(
                f"{self.url}/login",
                json={"username": self.username, "password": self.password},
            ).json()
            return response.get("success")
        except Exception as e:
            logger.error(f"Login test failed: {e}")
            return False

    def get_all_inbounds(self):
        self._get_session()
        url = f"{self.url}/panel/api/inbounds/list"
        try:
            response = self.session.get(url)
            return response.json()
        except requests.RequestException as e:
            logger.error(f"GET {url} failed: {e}")
            raise

    def add_user(self, inb_id, _uuid, subid, email, totalGB, expiryTime, flow) -> bool:
        self._get_session()
        try:
            new_client = {
                "id": _uuid,
                "enable": True,
                "email": email,
                "flow": flow,
                "totalGB": totalGB,
                "expiryTime": expiryTime,
                "subId": subid,
                "limitIp": 0,
            }
            settings = {"clients": [new_client]}

            response = self.session.post(
                f"{self.url}/panel/api/inbounds/addClient",
                json={
                    "id": inb_id,
                    "settings": json.dumps(settings),
                },
            )

            if response:
                return True
            logger.error(
                f"Create client failed (inb_id={inb_id}, email={email}): {response.text}"
            )
            return False
        except Exception as e:
            logger.error(f"Create client failed (inb_id={inb_id}, email={email}): {e}")
            return None

    def show_users(self, inb_id):
        self._get_session()
        try:
            all_inbounds = self.session.get(
                f"{self.url}/panel/api/inbounds/list"
            ).json()
            inbounds_list = all_inbounds.get("obj", [])

            for inbound in inbounds_list:
                if inbound.get("id") == inb_id:
                    return inbound.get("clientStats", [])

            return []
        except Exception as e:
            logger.error(f"Failed to fetch users for inbound {inb_id}: {e}")
            return None

    def get_user(self, email):
        self._get_session()
        try:
            response = self.session.get(
                f"{self.url}/panel/api/inbounds/getClientTraffics/{email}"
            ).json()
            return response.get("obj")
        except Exception as e:
            logger.error(f"Get user failed: {e}")
            return None

    def reset_traffic(self, inb_id, email) -> bool:
        self._get_session()
        try:
            response = self.session.post(
                f"{self.url}/panel/api/inbounds/{inb_id}/resetClientTraffic/{email}"
            )
            if response:
                return True
            return False
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
        self._get_session()
        _settings = {
            "id": user_id,
            "inbound_id": inb_id,
            "email": email,
            "totalGB": totalGB,
            "expiryTime": expirTime,
            "flow": inboud_flow,
            "subId": subid,
            "enable": True,
        }
        settings = {"clients": [_settings]}
        try:
            response = self.session.post(
                f"{self.url}/panel/api/inbounds/updateClient/{user_id}",
                json={
                    "id": inb_id,
                    "settings": json.dumps(settings),
                },
            ).json()
            logger.info(f"Client {email} updated successfully in inbound {inb_id}")
            if response.get("success"):
                return True
        except Exception as e:
            logger.error(f"Update client failed (inb_id={inb_id}, uuid={user_id}): {e}")
            return None

    def delete_client(self, inb_id, user_id) -> bool:
        self._get_session()
        try:
            response = self.session.post(
                f"{self.url}/panel/api/inbounds/{inb_id}/delClient/{user_id}"
            ).json()
            return response.get("success")
        except Exception as e:
            logger.error(f"Delete client failed: {e}")
            return False

    def server_status(self):
        self._get_session()
        try:
            result = self.session.get(f"{self.url}/panel/api/server/status").json()
            return result.get("obj")
        except Exception as e:
            logger.error(f"Server status failed: {e}")
            return None

    def online_users(self) -> list:
        self._get_session()
        try:
            result = self.session.post(f"{self.url}/panel/api/inbounds/onlines").json()
            return result.get("obj")
        except Exception as e:
            logger.error(f"Online users fetch failed: {e}")
            return None
