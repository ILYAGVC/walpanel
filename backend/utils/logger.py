import logging
import os


LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "app.log")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.WARNING,
)

logger = logging.getLogger("AppLogger")


def get_10_logs():
    """
    Get the last 10 logs from the log file
    """
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    return lines[-10:]
