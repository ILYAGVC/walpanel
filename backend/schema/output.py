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


class ClientsOutput(BaseModel):
    id: int
    uuid: str
    username: str
    email: Optional[str] = None
    status: bool
    is_online: bool
    data_limit: int
    used_data: int
    expiry_date: Optional[datetime] = None
    expiry_date_unix: Optional[int]
    sub_id: Optional[str] = None
    flow: Optional[str] = None

    class Config:
        from_attributes = True
