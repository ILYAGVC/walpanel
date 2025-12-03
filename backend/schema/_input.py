from datetime import datetime
from pydantic import BaseModel


class AdminInput(BaseModel):
    username: str
    password: str
    is_active: bool = True
    panel: str
    inbound_id: int = None
    traffic: float = 0.0
    return_traffic: bool = False
    expiry_date: datetime | None


class AdminUpdateInput(BaseModel):
    username: str
    password: str
    is_active: bool
    panel: str
    inbound_id: int
    traffic: float
    return_traffic: bool
    expiry_date: datetime | None


class PanelInput(BaseModel):
    panel_type: str = "3x-ui"
    name: str
    url: str
    username: str
    password: str
    is_active: bool = True
