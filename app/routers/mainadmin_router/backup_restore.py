from fastapi import APIRouter,UploadFile ,BackgroundTasks ,File , Depends
from fastapi.responses import FileResponse

from app.auth.auth_controller import mainadmin_required 
from app.db.engine import get_db
from app.log.logger_config import logger
import os

router = APIRouter(prefix="/backup_restore", tags=["Backup and Restore"])


db_path = "data/"
file_path = os.path.join(db_path, "walpanel.db")

@router.get("/backup")
async def get_backup(
    username: str = Depends(mainadmin_required),
):
    try:
        return FileResponse(
            file_path, 
            filename="walpanel.db", 
            media_type="application/octet-stream"
        )
    
    except Exception as e:
        logger.error(f"Error during backup: {e}")
        if not file_path:
            logger.error()
            return {
                "status": False,
                "message": "Database not found! pls check the logs."
            }
        
@router.post("/restore")
async def restore_backup(
        file: UploadFile = File(..., media_type='application/octet-stream'),
        username: str = Depends(mainadmin_required),
        background_tasks= BackgroundTasks()
):
    try:
        if not file:
            return {
                "status": False,
                "message": "No file uploaded."
            }
        file_location = os.path.join(db_path, "walpanel.db")
        with open(file_location, "wb") as f:
            f.write(file.file.read())

        background_tasks.add_task(os._exit, 0)# Drop container after restoring for restart :)
        return {
            "status": True,
            "message": "Database restored successfully."
        }
    

    except Exception as e:
        logger.error(f"Error during restore: {e}")
        return {
            "status": False,
            "message": f"Error restoring database pls check the logs."
        }

