from app.schema._input import CreateAdminInput, UpdateAdminInput
from app.db.models import Admin
from app.db.engine import get_db
from app.log.logger_config import logger
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status
import asyncio


class AdminOperations:

    def create_admin(self, db: Session, request: CreateAdminInput):
        existing_admin = (
            db.query(Admin).filter(Admin.username == request.username).first()
        )
        admins = db.query(Admin).count()

        if existing_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin with this username already exists.",
            )

        if admins >= 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="two admins are allowed in the free version.",
            )
        try:
            admin = Admin(
                username=request.username,
                password=request.password,
                panel_id=request.panel_id,
                inbound_id=request.inbound_id,
                traffic=request.traffic,
                days_remaining=request.days_remaining,
                is_active=request.is_active,
                is_banned=request.is_banned,
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            return admin
        except Exception as e:
            db.rollback()
            logger.exception(f"Error while creating admin: {e}")
            return None

    def delete_admin(self, db: Session, id: int):
        admin = db.query(Admin).filter(Admin.id == id).first()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin with this email not exist",
            )
        db.query(Admin).filter(Admin.id == id).delete()
        db.commit()
        return {"message": "successful"}

    def get_all_admins(self, db: Session):
        admins = db.query(Admin).all()
        return admins

    def edit_admin(self, db: Session, request: UpdateAdminInput):
        admin = db.query(Admin).filter(Admin.id == request.id).first()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin with this email not exist",
            )
        try:
            admin.panel_id = request.panel_id
            admin.inbound_id = request.inbound_id
            admin.traffic = request.traffic
            admin.days_remaining = request.days_remaining
            admin.is_active = request.is_active
            admin.is_banned = request.is_banned
            db.commit()
            db.refresh(admin)
            return admin
        except Exception as e:
            db.rollback()
            logger.exception(f"Error while editing admin: {e}")
            return None

    def login_admin(self, db: Session, username, password):
        admin = db.query(Admin).filter(Admin.username == username).first()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Email not found"
            )
        admin_password = admin.password
        if admin_password != password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
            )
        if not admin.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account is disabled.",
            )
        return {"message": "Login successful"}

    def get_admin_data(self, db: Session, username: str):
        admin = db.query(Admin).filter(Admin.username == username).first()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin with this username not exist",
            )
        return admin

    def reduce_traffic(self, db: Session, username: str, traffic_gb: int):
        admin = db.query(Admin).filter(Admin.username == username).first()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Admin with this username"
            )
        admin.traffic -= traffic_gb
        db.commit()
        db.refresh(admin)
        return admin

    def pre_opration_check(self, db: Session, username: str):
        admin = db.query(Admin).filter(Admin.username == username).first()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin with this username not exist",
            )
        elif admin.days_remaining == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Your days left is over",
            )
        elif admin.traffic == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Your traffic is over",
            )

        return True


class DailyOperation:

    async def decrease_days_remaining(self):
        db = next(get_db())
        admins = db.query(Admin).all()
        try:
            for admin in admins:
                if admin.days_remaining > 0:
                    admin.days_remaining -= 1
            db.commit()
        finally:
            db.close()
        await asyncio.sleep(86400)
        await self.decrease_days_remaining()


admin_operations = AdminOperations()
daily_operations = DailyOperation()
