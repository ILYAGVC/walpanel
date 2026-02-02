import os
import shutil
from fastapi import UploadFile, HTTPException
from backend.utils.logger import logger


def create_backup(db_path: str) -> str:
    """Create a backup of the database file"""
    if not os.path.exists(db_path):
        raise HTTPException(status_code=404, detail="Database file not found")

    backup_path = f"backup-{db_path}"
    shutil.copy2(db_path, backup_path)
    logger.info(f"Database backup created at {backup_path}")
    return backup_path


def restore_database(db_path: str, uploaded_file: UploadFile) -> None:
    """Restore database from uploaded file"""

    temp_path = f"{db_path}.temp"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)

        with open(temp_path, "rb") as f:
            header = f.read(16)
            if not header.startswith(b"SQLite format 3\x00"):
                raise HTTPException(status_code=400, detail="Invalid database file")

        # Replace the current db
        shutil.move(temp_path, db_path)
        logger.info(f"Database restored from uploaded file")

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        logger.error(f"Failed to restore database: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to restore database: {str(e)}"
        )
