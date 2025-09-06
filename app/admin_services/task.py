from app.admin_services.api import PanelAPI
from app.oprations.panel import panel_operations
from app.oprations.admin import admin_operations
from app.schema._input import CreateUserInput, UpdateUserInput
from app.log.logger_config import logger
from fastapi.responses import JSONResponse
from fastapi import status
from datetime import datetime
from uuid import uuid4
import string
import secrets


class Task:
    def get_sublinks(self, db, username):
        try:
            admin = admin_operations.get_admin_data(db, username)
            panel = panel_operations.panel_data(db, admin.panel_id)
            return {"result": f"https://{panel.sub}/"}
        except Exception as e:
            logger.error(f"Error getting sublinks: {e}")
            return JSONResponse(
                content={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def check_admin_traffic(self, db, username, _traffic):
        try:
            admin = admin_operations.get_admin_data(db, username)

            if admin.traffic < _traffic:
                return False

            return True
        except Exception as e:
            return False

    def reduce_admin_traffic(self, db, username, _traffic):
        try:
            admin_operations.reduce_traffic(db, username, _traffic)
        except Exception as e:
            return False

    def get_users(self, db, username):
        """This function retrieves the list of users for a specific admin.
        Example return value:
        {
            "clients": [
                {
                    "email": "primeZ",
                    "online": True,
                    "id": "b32a3afb-7604-44ec-8a48-65d284f7bd84",
                    "totalGB": 10,
                    "totalUsage": 5,
                    "expiryTime": "2026-12-31",
                    "enable": True,
                    "subId": "mld0xo12ktdu0ni0"
                }
            ]
        }
        """
        client_list = []
        _online_users = []

        try:
            admin = admin_operations.get_admin_data(db, username)
            panel = panel_operations.panel_data(db, admin.panel_id)

            result = PanelAPI(panel.url, panel.username, panel.password).show_users(
                admin.inbound_id
            )
            _online_users = PanelAPI(
                panel.url, panel.username, panel.password
            ).online_users()

            for client in result:
                try:
                    total_usage = (client.up + client.down) / (1024**3)
                    client_online = (
                        client.email in _online_users
                    )  # Check if client is online
                    client_list.append(
                        {
                            "email": client.email,
                            "online": client_online,
                            "id": client.id,
                            "totalGB": client.total_gb / (1024**3),
                            "totalUsage": total_usage,
                            "expiryTime": datetime.fromtimestamp(
                                client.expiry_time / 1000
                            ).strftime("%Y-%m-%d"),
                            "enable": client.enable,
                            "subId": client.sub_id,
                        }
                    )
                except Exception as e:
                    logger.warning(f"Failed to process client {client.email}: {e}")
        except Exception as e:
            logger.error(f"Error fetching user list: {e}")
            return {
                "clients": client_list,
                "error": "Failed to fetch user list, try again.",
            }
        return {"clients": client_list}

    async def total_users_in_inbound(self, db, username: str, retry: int = 0) -> int:
        client_count = 0
        admin = admin_operations.get_admin_data(db, username)
        panel = panel_operations.panel_data(db, admin.panel_id)
        try:
            result = PanelAPI(panel.url, panel.username, panel.password).show_users(
                admin.inbound_id
            )

            client_count = len(result)
        except Exception as e:
            logger.error(f"fetching user list: {e} and returned 0")

        finally:
            return client_count

    def create_user(self, db, username: str, request: CreateUserInput):
        if not self.check_admin_traffic(db, username, request.totalGB):
            return JSONResponse(
                content={"error": "Traffic limit reached"},
                status_code=status.HTTP_403_FORBIDDEN,
            )

        try:
            admin = admin_operations.get_admin_data(db, username)
            panel = panel_operations.panel_data(db, admin.panel_id)

            _uuid = str(uuid4())
            subid = generate_secure_random_text(16)

            result = PanelAPI(panel.url, panel.username, panel.password).add_user(
                admin.inbound_id,
                _uuid,
                subid,
                request.email,
                int(request.totalGB * (1024**3)),  # coverted to byte
                request.expiryTime,
                admin.inbound_flow,
            )
            if result:
                _traffic = round(request.totalGB, 1)
                self.reduce_admin_traffic(db, username, _traffic)
        except Exception as e:
            return JSONResponse(
                content={"error": f"Create user failed: {str(e)}"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete_client(self, db, username: str, user_id: str, name: str):
        try:
            admin = admin_operations.get_admin_data(db, username)
            panel = panel_operations.panel_data(db, admin.panel_id)

            # returned remining traffic to the admin
            client = PanelAPI(panel.url, panel.username, panel.password).get_user(name)
            client_usage_traffic = (client.up + client.down) / (1024**3)
            client_traffic = client.total / (1024**3)
            _traffic = round((client_traffic - client_usage_traffic), 1)

            result = PanelAPI(panel.url, panel.username, panel.password).delete_client(
                admin.inbound_id,
                user_id,
            )
            admin_operations.Increased_traffic(db, admin.username, _traffic)
        except Exception as e:
            return JSONResponse(
                content={"error": f"Delete client failed: {str(e)}"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update_client(self, db, username: str, user_id: str, request: UpdateUserInput):
        if not self.check_admin_traffic(db, username, request.totalGB):
            return JSONResponse(
                content={"error": "Traffic limit reached"},
                status_code=status.HTTP_403_FORBIDDEN,
            )
        try:
            admin = admin_operations.get_admin_data(db, username)
            panel = panel_operations.panel_data(db, admin.panel_id)

            # returned remining traffic to the admin
            client = PanelAPI(panel.url, panel.username, panel.password).get_user(
                request.email
            )
            client_usage_traffic = (client.up + client.down) / (1024**3)
            client_traffic = client.total / (1024**3)
            _traffic = round(client_traffic - client_usage_traffic, 1)
            admin_operations.Increased_traffic(db, admin.username, _traffic)

            result = PanelAPI(panel.url, panel.username, panel.password).update_client(
                admin.inbound_id,
                user_id,
                request.email,
                int(request.totalGB * (1024**3)),
                request.expiryTime,
                admin.inbound_flow,
                request.subid,
            )
            if result:
                self.reduce_admin_traffic(db, username, request.totalGB)

            return JSONResponse(content=result, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(
                content={"error": f"Update client failed: {e}"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def reset_client_traffic(self, db, username: str, email: str):
        admin = admin_operations.get_admin_data(db, username)
        panel = panel_operations.panel_data(db, admin.panel_id)
        client = PanelAPI(
            panel.url,
            panel.username,
            panel.password,
        ).get_user(email)
        client_usage_traffic = (client.up + client.down) / (1024**3)
        client_traffic = client.total / (1024**3)
        _traffic = round((client_traffic - client_usage_traffic), 1)
        if not self.check_admin_traffic(db, username, _traffic):
            return JSONResponse(
                content={"error": "Traffic limit reached"},
                status_code=status.HTTP_403_FORBIDDEN,
            )

        try:
            result = PanelAPI(
                panel.url,
                panel.username,
                panel.password,
            ).reset_traffic(
                admin.inbound_id,
                email,
            )

            if result:
                # returned remining traffic to the admin
                admin_operations.Increased_traffic(db, admin.username, _traffic)

                self.reduce_admin_traffic(db, username, _traffic)

            return JSONResponse(content=result, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(
                content={"error": f"Reset traffic failed: {str(e)}"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


admin_task = Task()


def generate_secure_random_text(length=16):
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))
