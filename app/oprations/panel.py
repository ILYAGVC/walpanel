from sqlalchemy.orm import Session
from app.schema._input import CreatePanelInput
from app.db.models import Panel
from fastapi.exceptions import HTTPException
from fastapi import status
from app.admin_services.api import panels_api
from app.log.logger_config import logger


class PanelOperations:

    def create_panel(self, db: Session, request: CreatePanelInput):
        panel_exception = db.query(Panel).filter(Panel.url == request.url).first()

        if panel_exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Panel with this URL already exists.",
            )

        if not panels_api.login(request.url, request.username, request.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Login failed.",
            )
        try:
            new_panel = Panel(
                name=request.name,
                url=request.url,
                sub=request.sub,
                username=request.username,
                password=request.password,
            )
            db.add(new_panel)
            db.commit()
            db.refresh(new_panel)
            return new_panel
        except Exception as e:
            db.rollback()
            logger.error(f"Error while creating panel")
            return None

    def edit_panel(self, db: Session, request: CreatePanelInput, id: int):
        panel = db.query(Panel).filter(Panel.id == id).first()
        if not panel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Panel with this id not exist",
            )
        try:
            panel.name = request.name
            panel.url = request.url
            panel.sub = request.sub
            panel.username = request.username
            panel.password = request.password
            db.commit()
            db.refresh(panel)
            return panel
        except Exception as e:
            db.rollback()
            logger.exception("Error while editing panel")
            return None

    def delete_panel(self, db: Session, id: int):
        panel = db.query(Panel).filter(Panel.id == id).first()
        if not panel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Panel with this name not exist",
            )
        db.query(Panel).filter(Panel.id == id).delete()
        db.commit()
        return {"messsage": "successful"}

    def get_panels(self, db: Session):
        panels = db.query(Panel).all()
        return panels

    async def get_panel_status(self, db: Session):
        panels = db.query(Panel).all()
        statuses = []
        if panels:
            for panel in panels:
                panel_status = await panels_api.server_status(
                    panel.url, panel.username, panel.password
                )
                statuses.append({"panel_id": panel.id, "status": panel_status})
        return statuses

    def panel_data(self, db: Session, id: int):
        panel = db.query(Panel).filter(Panel.id == id).first()
        if not panel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Panel with this name"
            )
        return panel


panel_operations = PanelOperations()
