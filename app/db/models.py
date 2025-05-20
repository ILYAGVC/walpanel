from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.engine import Base


class Panel(Base):
    __tablename__ = "panels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    sub = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    admins = relationship("Admin", back_populates="panel")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String, nullable=False)
    panel_id = Column(Integer, ForeignKey("panels.id"), nullable=False)
    inbound_id = Column(Integer, default=1)
    traffic = Column(Integer, default=0)
    expiry_time = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)

    panel = relationship("Panel", back_populates="admins")


class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String, default="en")
