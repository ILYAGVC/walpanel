from fastapi import APIRouter, Request, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from app.auth.auth_controller import mainadmin_required
from app.db.engine import get_db
from app.oprations.panel import panel_operations
from app.oprations.admin import admin_operations
from sqlalchemy.orm import Session


templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/dashboard", tags=["Main admin dashboard"])


@router.get("/")
async def dashboard(
    request: Request,
    user: str = Depends(mainadmin_required),
    db: Session = Depends(get_db),
):
    panels = panel_operations.get_panels(db)
    admins = admin_operations.get_all_admins(db)
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user, "panels": panels, "admins": admins},
    )


@router.get("/logout/")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return JSONResponse(content={"message": "Logged out", "redirect": "/login/"})


@router.get("/panels/")
async def panels(
    request: Request,
    user: str = Depends(mainadmin_required),
    db: Session = Depends(get_db),
):
    panels = panel_operations.get_panels(db)
    return templates.TemplateResponse(
        "panels.html", {"request": request, "panels": panels}
    )


@router.get("/admins/")
async def admins(
    request: Request,
    user: str = Depends(mainadmin_required),
    db: Session = Depends(get_db),
):
    admins = admin_operations.get_all_admins(db)
    return templates.TemplateResponse(
        "admins.html", {"request": request, "user": user, "admins": admins}
    )


@router.get("/settings/")
async def settings(
    request: Request,
    user: str = Depends(mainadmin_required),
    db: Session = Depends(get_db),
):
    return templates.TemplateResponse(
        "settings.html", {"request": request, "user": user}
    )


@router.get("/receipts/")
async def receipts(
    request: Request,
    user: str = Depends(mainadmin_required),
    db: Session = Depends(get_db),
):
    return templates.TemplateResponse(
        "receipts.html", {"request": request, "user": user}
    )
