from app.db.models import (
    Panel,
    Admin,
    Setting,
    Plans,
    CardNumber,
    BotSettings,
    HelpMessage,
    RegisteringMessage,
    PaymentGatewaykeys,
    PurchaseHistory,
)
from app.db.engine import SessionLocal
from app.log.logger_config import logger
from datetime import date, datetime, timedelta


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
                    "days_remaining": admin.expiry_time,
                    "is_active": admin.is_active,
                    "panel": admin.panel.name,
                }
                for admin in admins
            ]
        except Exception as e:
            logger.error(f"Error in get_all_admins in bot: {e}")
            return None

    def check_loged_in(self, chat_id):
        try:
            admin = self.db.query(Admin).filter_by(chat_id=chat_id).first()
            if admin:
                return True
            return False
        except Exception as e:
            logger.error(f"Error in check_loged_in in bot: {e}")
            return False

    def login_admin(self, username, password, chat_id):
        try:
            admin = self.db.query(Admin).filter_by(username=username).first()
            if admin:
                if admin.password == password:
                    admin.chat_id = chat_id
                    self.db.commit()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error in login_admin in bot: {e}")
            return False

    def logout_admin(self, chat_id):
        try:
            admin = self.db.query(Admin).filter_by(chat_id=chat_id).first()
            if admin:
                admin.chat_id = 0
                self.db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error in logout_admin in bot: {e}")
            return False

    def create_admin(self, username, password, panel_id, inbound_id, expiry_time: date):
        try:
            admin = Admin(
                username=username,
                password=password,
                panel_id=panel_id,
                inbound_id=inbound_id,
                traffic=0,
                expiry_time=expiry_time,
            )
            self.db.add(admin)
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error in create_admin in bot: {e}")
            return False

    def get_admin_by_chat_id(self, chat_id):
        try:
            admin = self.db.query(Admin).filter_by(chat_id=chat_id).first()
            if admin:
                return {
                    "username": admin.username,
                    "password": admin.password,
                    "panel_id": admin.panel_id,
                    "traffic": admin.traffic,
                    "expiry_time": admin.expiry_time,
                    "is_active": admin.is_active,
                }
            return None
        except Exception as e:
            logger.error(f"Error in get_admin_by_chat_id in bot: {e}")
            return None

    def purchase_confirmation(self, chat_id, traffic, days):
        try:
            admin = self.db.query(Admin).filter_by(chat_id=chat_id).first()
            if admin:
                admin.traffic += traffic
                admin.expiry_time = admin.expiry_time + timedelta(days=days)
                self.db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error in purchase_confirmation in bot: {e}")
            return False


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
                    "id": panel.id,
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

    def get_panel_by_id(self, id):
        try:
            panel = self.db.query(Panel).filter_by(id=id).first()
            if panel:
                return {
                    "id": panel.id,
                    "name": panel.name,
                    "url": panel.url,
                    "sub": panel.sub,
                }
            return False
        except Exception as e:
            logger.error(f"Error in get_panel_by_id in bot: {e}")


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

    async def get_card_method(self):
        try:
            setting = self.db.query(Setting).first()
            if setting:
                return setting.card_payment_enabled
            else:
                return False
        except Exception as e:
            logger.error(f"Error in get_card_method in bot: {e}")
            return None

    async def change_card_method_status(self):
        try:
            status = await self.get_card_method()
            new_status = not status
            self.db.query(Setting).update({"card_payment_enabled": new_status})
            self.db.commit()
            return new_status
        except Exception as e:
            logger.error(f"Error in change_card_method_status in bot: {e}")
            return None

    async def get_intermediary_gateway(self):
        try:
            setting = self.db.query(Setting).first()
            if setting:
                return setting.Intermediary_payment_gateway
            else:
                return False
        except Exception as e:
            logger.error(f"Error in get_intermediary_gateway in bot: {e}")

    async def change_intermediary_gateway_status(self):
        try:
            status = await self.get_intermediary_gateway()
            new_status = not status
            self.db.query(Setting).update({"Intermediary_payment_gateway": new_status})
            self.db.commit()
            return new_status
        except Exception as e:
            logger.error(f"Error in change_intermediary_gateway_status in bot: {e}")
            return None


class PlansQuery:
    def __init__(self):
        self.db = SessionLocal()

    def get_plans(self):
        try:
            plans = self.db.query(Plans).all()
            if not plans:
                return False
            return [
                {
                    "id": plan.id,
                    "price": plan.price,
                    "traffic": plan.traffic,
                    "deadline": plan.days,
                }
                for plan in plans
            ]
        except Exception as e:
            logger.error(f"Error in get_plans in bot: {e}")
            return None

    def add_plan(self, traffic, deadline, price):
        try:
            plan = Plans(traffic=traffic, days=deadline, price=price)
            self.db.add(plan)
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error in add_plan in bot: {e}")
            return False

    def delete_plan(self, id):
        try:
            plan = self.db.query(Plans).filter(Plans.id == id).first()
            if not plan:
                return False
            self.db.delete(plan)
            self.db.commit()
            self.reorder_ids()
            return True
        except Exception as e:
            logger.error(f"Error in delete_plan in bot: {e}")
            return False

    def edit_plan(self, id, traffic, deadline, price):
        try:
            plan = self.db.query(Plans).filter(Plans.id == id).first()
            if not plan:
                return False
            plan.traffic = traffic
            plan.days = deadline
            plan.price = price
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error in edit_plan in bot: {e}")
            return False

    def reorder_ids(self):
        try:
            plans = self.db.query(Plans).order_by(Plans.id).all()
            for index, plan in enumerate(plans, start=1):
                plan.id = index
            self.db.commit()
            return True
        except:
            return False

    def get_a_plan_by_id(self, plan_id):
        try:
            plan = self.db.query(Plans).filter(Plans.id == plan_id).first()
            if not plan:
                return False
            return {
                "traffic": plan.traffic,
                "days": plan.days,
                "price": plan.price,
                "deadline": plan.days,
            }
        except Exception as e:
            logger.error(f"Error in get_a_plan_by_id in bot: {e}")
            return None


class CardQuery:
    def __init__(self):
        self.db = SessionLocal()

    def get_card(self):
        try:
            card = self.db.query(CardNumber).filter(CardNumber.id == 1).first()
            if not card:
                card_number = 123456789
                return card_number

            card_number = card.number
            return card_number

        except Exception as e:
            logger.error(f"Error in get_card in bot: {e}")
            return None

    def add_card(self, new_card_number):
        try:
            card = self.db.query(CardNumber).first()
            if card:
                card.number = new_card_number
                self.db.commit()
                return True
            else:
                new_card = CardNumber(number=new_card_number)
                self.db.add(new_card)
                self.db.commit()
                return True
        except Exception as e:
            logger.error(f"Error in add_card in bot: {e}")
            return False


class BotSettingsQuery:
    def __init__(self):
        self.db = SessionLocal()

    def get_start_notif(self):
        try:
            setting = self.db.query(BotSettings).first()
            return setting.start_notif
        except Exception as e:
            logger.error(f"Error in get_start_notif in bot: {e}")

    def change_start_notif(self, new_value):
        try:
            setting = self.db.query(BotSettings).first()
            if setting:
                setting.start_notif = new_value
                self.db.commit()
                return True
            else:
                new_setting = BotSettings(start_notif=new_value)
                self.db.add(new_setting)
                self.db.commit()
                return True
        except Exception as e:
            logger.error(f"Error in change_start_notif in bot: {e}")
            return False

    def get_create_notif(self):
        try:
            setting = self.db.query(BotSettings).first()
            return setting.create_notif
        except Exception as e:
            logger.error(f"Error in get_create_notif in bot: {e}")

    def change_create_notif(self, new_value):
        try:
            setting = self.db.query(BotSettings).first()
            if setting:
                setting.create_notif = new_value
                self.db.commit()
                return True
            else:
                new_setting = BotSettings(create_notif=new_value)
                self.db.add(new_setting)
                self.db.commit()
                return True
        except Exception as e:
            logger.error(f"Error in change_create_notif in bot: {e}")

    def get_delete_notif(self):
        try:
            setting = self.db.query(BotSettings).first()
            return setting.delete_notif
        except Exception as e:
            logger.error(f"Error in get_delete_notif in bot: {e}")

    def change_delete_notif(self, new_value):
        try:
            setting = self.db.query(BotSettings).first()
            if setting:
                setting.delete_notif = new_value
                self.db.commit()
                return True
            else:
                new_setting = BotSettings(delete_notif=new_value)
                self.db.add(new_setting)
                self.db.commit()
                return True
        except Exception as e:
            logger.error(f"Error in change_delete_notif in bot: {e}")


class HelpMessageQuery:
    def __init__(self):
        self.db = SessionLocal()

    def get_help_message(self):
        try:
            help_message = self.db.query(HelpMessage).first()
            if not help_message:
                return "no help message found!"
            return help_message.message
        except Exception as e:
            logger.error(f"Error in get_help_message in bot: {e}")
            return None

    def change_help_message(self, new_message):
        try:
            help_message = self.db.query(HelpMessage).first()
            if help_message:
                help_message.message = new_message
                self.db.commit()
                return True
            else:
                new_message = HelpMessage(message=new_message)
                self.db.add(new_message)
                self.db.commit()
                return True
        except Exception as e:
            logger.error(f"Error in change_help_message in bot: {e}")
            return None


class RegisteringMessageQuery:
    def __init__(self):
        self.db = SessionLocal()

    def get_registering_message(self):
        try:
            registering_message = self.db.query(RegisteringMessage).first()
            if not registering_message:
                return "no help message found!"
            return registering_message.message
        except Exception as e:
            logger.error(f"Error in get_help_message in bot: {e}")
            return None

    def chage_registering_message(self, new_message):
        try:
            registering_message = self.db.query(RegisteringMessage).first()
            if registering_message:
                registering_message.message = new_message
                self.db.commit()
                return True
            else:
                new_message = RegisteringMessage(message=new_message)
                self.db.add(new_message)
                self.db.commit()
                return True
        except Exception as e:
            logger.error(f"Error in change_help_message in bot: {e}")
            return None


class PaymentGatewayKeysQuery:
    def __init__(self):
        self.db = SessionLocal()

    def get_intermediary_gateway_key(self):
        try:
            key = self.db.query(PaymentGatewaykeys).first()
            if not key:
                return "xxxXXXxxx"
            return key.Intermediary_gateway_key
        except Exception as e:
            logger.error(f"Error in get_intermediary_gateway_key in bot: {e}")
            return None

    async def change_intermediary_gateway_key(self, new_api_key: str):
        try:
            key = self.db.query(PaymentGatewaykeys).first()
            if key:
                key.Intermediary_gateway_key = new_api_key
            else:
                new_key = PaymentGatewaykeys(Intermediary_gateway_key=new_api_key)
                self.db.add(new_key)
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error in change_intermediary_gateway_key in bot: {e}")
            return None


class PurchaseHistoryQuery:
    def __init__(self):
        self.db = SessionLocal()

    async def add_purchase_history(
        self,
        chat_id: int,
        amount: int,
        order_id: str,
        timestamp: datetime,
        status: bool,
    ):
        try:
            # Convert datetime to date for database storage
            purchase_date = (
                timestamp.date() if isinstance(timestamp, datetime) else timestamp
            )
            purchase = PurchaseHistory(
                chat_id=chat_id,
                amount=amount,
                order_id=order_id,
                purchase_date=purchase_date,
                status="paid" if status else "failed",
            )
            self.db.add(purchase)
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error in add_purchase_history in bot: {e}")
            return False


admins_query = AdminQuery()
panels_query = PanelQuery()
plans_query = PlansQuery()
card_query = CardQuery()
bot_settings_query = BotSettingsQuery()
help_message_query = HelpMessageQuery()
registering_message_query = RegisteringMessageQuery()
settings_query = SettingsQuery()
payment_gateway_query = PaymentGatewayKeysQuery()
purchase_history_query = PurchaseHistoryQuery()
