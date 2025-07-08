from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.auth.auth_controller import get_current_user
from app.db.engine import get_db
from app.oprations.admin import admin_operations
from app.oprations.panel import panel_operations
from sqlalchemy.orm import Session
from app.admin_services.task import admin_task
from datetime import date


templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/admin-dashboard", tags=["Admin dashboard"])


@router.get("/")
def dashboard(
    request: Request,
    username: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
        },
    )


@router.get("/dashboard-data")
def get_dashboard_data(
    db: Session = Depends(get_db),
    username: dict = Depends(get_current_user),
):
    admin = admin_operations.get_admin_data(db, username["username"])
    get_clients = admin_task.get_users(db, username["username"])
    clients = get_clients.get("clients", [])
    total_clients = len([c for c in clients if "email" in c and c["email"]])

    return {
        "totalClients": total_clients,
        "availableDataGB": admin.traffic,
        "daysRemaining": (admin.expiry_time - date.today()).days,
    }


@router.get("/news")
async def get_news(
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user),
):
    news = await panel_operations.get_news(db)
    return news


@router.get("/clients/")
def get_users(
    request: Request,
    db: Session = Depends(get_db),
    username: dict = Depends(get_current_user),
):
    return templates.TemplateResponse(
        "admin/clients.html",
        {
            "request": request,
        },
    )


@router.get("/clients-data")
def get_clients_data(
    db: Session = Depends(get_db),
    username: dict = Depends(get_current_user),
):
    data = admin_task.get_users(db, username["username"])
    sublink = admin_task.get_sublinks(db, username["username"])
    return {"data": data, "sublink": sublink}

@router.get("/plans")
def get_plans(
    request: Request,
    db: Session = Depends(get_db),
    username: dict = Depends(get_current_user),
):
    return templates.TemplateResponse(
        "admin/plans.html",
        {
            "request": request,
        },
    )