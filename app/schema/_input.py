from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class CreatePanelInput(BaseModel):
    name: str
    url: str
    sub: str
    username: str
    password: str


class CreateAdminInput(BaseModel):
    username: str
    password: str
    panel_id: int = 1
    inbound_id: int = 1
    traffic: int = 0
    days_remaining: int = 0
    is_active: bool = True
    is_banned: bool = False


class UpdateAdminInput(BaseModel):
    id: int
    panel_id: int
    inbound_id: int
    traffic: int
    days_remaining: int
    is_active: bool = True
    is_banned: bool = False


class CreateUserInput(BaseModel):
    email: str
    totalGB: float
    expiryTime: int


class UpdateUserInput(BaseModel):
    email: str
    expiryTime: int
    subid: str
    totalGB: int


class CreateNews(BaseModel):
    message: str
