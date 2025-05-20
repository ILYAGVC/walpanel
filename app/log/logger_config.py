import logging

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
