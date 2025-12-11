from sqlalchemy.orm import Session

from backend.schema._input import PanelInput
from backend.services.sanaei import APIService
from backend.utils.logger import logger


async def create_new_panel(db: Session, panel_input: PanelInput) -> bool:
    if panel_input.panel_type == "3x-ui":
        try:
            connection = await APIService(
                panel_input.url, panel_input.username, panel_input.password
            ).test_connection()

            if connection is None or not connection.cpu:
                logger.warning(
                    f"Panel validation failed: {panel_input.name} - missing required fields"
                )
                return False

            logger.info(f"Panel validated successfully: {panel_input.name}")
            return True
        except Exception as e:
            logger.error(f"Error connecting to panel {panel_input.url}: {str(e)}")
            return False


async def update_a_panel(db: Session, panel_input: PanelInput) -> bool:
    if panel_input.panel_type == "3x-ui":
        try:
            connection = await APIService(
                panel_input.url, panel_input.username, panel_input.password
            ).test_connection()

            if connection is None or not connection.cpu:
                logger.warning(
                    f"Panel validation failed during update: {panel_input.name} - missing required fields"
                )
                return False

            logger.info(
                f"Panel validated successfully during update: {panel_input.name}"
            )
            return True
        except Exception as e:
            logger.error(
                f"Error connecting to panel {panel_input.url} during update: {str(e)}"
            )
            return False
