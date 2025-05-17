from app.db.models import Panel, Admin
from app.db.engine import SessionLocal
from app.log.logger_config import logger
from datetime import date


class AdminQuery:
    def __init__(self):
        self.db = SessionLocal()

    async def get_all_admins(self):
        try:
            admins = self.db.query(Admin).all()
            if not admins:
                return "no admins found!"
            return [
                {
                    "username": admin.username,
                    "traffic": admin.traffic,
                    "days_remaining": (admin.expiry_time - date.today()).days,
                    "is_active": admin.is_active,
                }
                for admin in admins
            ]
        except Exception as e:
            logger.error(f"Error in get_all_admins in bot: {e}")
            return None


class PanelQuery:
    def __init__(self):
        self.db = SessionLocal()

    async def get_all_panels(self):
        try:
            panels = self.db.query(Panel).all()
            if not panels:
                return "no panels found!"
            return [
                {
                    "name": panel.name,
                    "url": panel.url,
                    "sub": panel.sub,
                }
                for panel in panels
            ]
        except Exception as e:
            logger.error(f"Error in get_all_panels in bot: {e}")
            return None


admins_query = AdminQuery()
panels_query = PanelQuery()
