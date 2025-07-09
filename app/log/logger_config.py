import logging
import os

logging.basicConfig(
    filename="data/app.log",
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
    log_file = "data/app.log"
    if not os.path.exists(log_file):
        return []
    with open(log_file, "r") as f:
        lines = f.readlines()
    return lines[-10:]