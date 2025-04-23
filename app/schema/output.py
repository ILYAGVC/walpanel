from pydantic import BaseModel
from typing import List


class PanelDisplay(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class PanelOutput(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class PanelsListOutput(BaseModel):
    panels: list[PanelOutput]


class AdminDisplay(BaseModel):
    username: str
    password: str
    traffic: int

    class Config:
        orm_mode = True


class AdminOutput(BaseModel):
    email: str
    password: str
    panel_id: int
    inbound_id: int
    traffic: int
    debting_days: int
    is_active: bool
    is_banned: bool

    class Config:
        orm_mode = True


class AdminsListOutout(BaseModel):
    admins: list[AdminOutput]


class Token(BaseModel):
    access_token: str
    token_type: str
