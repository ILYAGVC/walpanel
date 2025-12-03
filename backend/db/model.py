from .engin import Base
from sqlalchemy import Column, DateTime, Float, Integer, String, Boolean


class Admins(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    panel = Column(String, nullable=False)
    inbound_id = Column(Integer, nullable=True)
    traffic = Column(Float, default=0.0)
    return_traffic = Column(Boolean, default=False)
    expiry_date = Column(DateTime, nullable=True)


class Panels(Base):
    __tablename__ = "panels"

    id = Column(Integer, primary_key=True, index=True)
    panel_type = Column(String, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    url = Column(String, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
