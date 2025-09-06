import psutil
import time
from fastapi import HTTPException
from log.logger_config import logger
from schema.output import ServerInfo


async def get_server_info() -> ServerInfo:
    try:
        return ServerInfo(
            cpu=psutil.cpu_percent(interval=0.5),
            memory_total=psutil.virtual_memory().total,
            memory_used=psutil.virtual_memory().used,
            memory_percent=psutil.virtual_memory().percent,
        )
    except Exception as e:
        logger.error(f"error when get server info: {e}")
        raise HTTPException(
            status_code=500, detail="error when get server info, please check the logs"
        )
