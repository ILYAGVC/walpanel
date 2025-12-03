from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class ResponseModel(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None


class AdminOutput(BaseModel):
    id: int
    username: str
    is_active: bool
    panel: str
    inbound_id: Optional[int]
    traffic: float
    return_traffic: bool
    expiry_date: Optional[datetime]

    class Config:
        from_attributes = True


class PanelOutput(BaseModel):
    id: int
    panel_type: str
    name: str
    url: str
    is_active: bool

    class Config:
        from_attributes = True
