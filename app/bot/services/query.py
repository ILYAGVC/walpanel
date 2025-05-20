from app.db.models import Panel, Admin, Setting
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
                return False
            return [
                {
                    "username": admin.username,
                    "traffic": admin.traffic,
                    "days_remaining": (admin.expiry_time - date.today()).days,
                    "panel": admin.panel.name if admin.panel else None,
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
                return False
            return [
                {
                    "name": panel.name,
                    "url": panel.url,
                    "username": panel.username,
                    "password": panel.password,
                    "sub": panel.sub,
                }
                for panel in panels
            ]
        except Exception as e:
            logger.error(f"Error in get_all_panels in bot: {e}")
            return None


class SettingsQuery:
    def __init__(self):
        self.db = SessionLocal()

    async def get_language(self):
        try:
            settings = self.db.query(Setting).filter(Setting.id == 1).first()
            if not settings:
                return "en"
            return settings.language
        except Exception as e:
            logger.error(f"Error in get_language in bot: {e}")
            return None

    async def change_language(self, new_language):
        try:
            settings = self.db.query(Setting).filter(Setting.id == 1).first()
            if not settings:
                self.db.add(Setting(id=1, language=new_language))
                self.db.commit()
                return True

            settings.language = new_language
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error in change_language in bot: {e}")
            return None


admins_query = AdminQuery()
panels_query = PanelQuery()
settings_query = SettingsQuery()
