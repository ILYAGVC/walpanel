from sqlalchemy.orm import Session

from backend.schema._input import PanelInput
from backend.services.sanaei import APIService


async def create_new_panel(db: Session, panel_input: PanelInput) -> bool:
    if panel_input.panel_type == "3x-ui":
        try:
            connection = await APIService(
                panel_input.url, panel_input.username, panel_input.password
            ).test_connection()

            if connection is None or not connection.cpu:
                return False

            return True
        except Exception as e:
            return False


async def update_a_panel(db: Session, panel_input: PanelInput) -> bool:
    if panel_input.panel_type == "3x-ui":
        try:
            connection = await APIService(
                panel_input.url, panel_input.username, panel_input.password
            ).test_connection()

            if connection is None or not connection.cpu:
                return False

            return True
        except Exception as e:
            return False
