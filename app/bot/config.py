import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

TOKEN = os.getenv("BOT_TOKEN")
MAIN_ADMIN = int(os.getenv("ADMIN_CHAT_ID"))
PANEL_ADDRESS = str(os.getenv("PANEL_ADDRESS"))
