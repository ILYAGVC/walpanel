from fastapi import Depends, HTTPException, Request, Cookie
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from app.oprations.admin import admin_operations
from app.db.engine import get_db
from dotenv import load_dotenv

import os
import jwt

router = APIRouter(prefix="/login", tags=["Login"])
templates = Jinja2Templates(directory="templates")

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


SECRET_KEY = "1a9f4031b27ca0f58840009a9f48a37a27fba5260757617ed187177b29c91d85"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", auto_error=False)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    access_token: str = Cookie(None),
):
    if not token or token == "null":
        token = access_token

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        is_mainadmin = username == USERNAME

        return {"username": username, "is_mainadmin": is_mainadmin}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def mainadmin_required(user: dict = Depends(get_current_user)):
    if not user["is_mainadmin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return user


@router.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    if form_data.username == USERNAME and form_data.password == PASSWORD:
        token = create_access_token({"sub": form_data.username})

        if "application/json" in request.headers.get("accept", ""):
            return JSONResponse(content={"access_token": token, "token_type": "bearer"})

        response = RedirectResponse(url="/dashboard/", status_code=303)
        response.set_cookie(
            key="access_token", value=token, httponly=True, samesite="Lax", secure=True
        )
        return response

    admin = admin_operations.login_admin(
        db=db, username=form_data.username, password=form_data.password
    )
    if admin:
        token = create_access_token({"sub": form_data.username})

        if "application/json" in request.headers.get("accept", ""):
            return JSONResponse(content={"access_token": token, "token_type": "bearer"})

        response = RedirectResponse(url="/admin-dashboard/", status_code=303)
        response.set_cookie(
            key="access_token", value=token, httponly=True, samesite="Lax", secure=True
        )
        print(response)
        return response

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error_message": "Invalid username or password."},
    )
