from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from backend.schema.output import ResponseModel, AdminOutput
from backend.schema._input import AdminInput, AdminUpdateInput, PanelInput
from backend.db import crud
from backend.db.engin import get_db
from backend.services import create_new_panel, update_a_panel

router = APIRouter(prefix="/superadmin", tags=["superadmin"])


@router.post("/admin", description="create a new admin", response_model=ResponseModel)
async def create_admin(admin_input: AdminInput, db: Session = Depends(get_db)):
    if crud.get_admin_by_username(db, admin_input.username):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "message": "Admin with this username already exists",
            },
        )

    crud.add_admin(db, admin_input)
    return ResponseModel(
        success=True,
        message="Admin created successfully",
    )


@router.put("/admin/{admin_id}", response_model=ResponseModel)
async def update_admin(
    admin_id: int, admin_input: AdminUpdateInput, db: Session = Depends(get_db)
):
    if not crud.get_admin_by_username(db, admin_input.username):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Admin not found",
            },
        )
    update_admin = crud.update_admin_values(db, admin_id, admin_input)
    if update_admin:
        return ResponseModel(
            success=True,
            message="Admin updated successfully",
        )


@router.delete("/admin/{admin_id}", response_model=ResponseModel)
async def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    remove_admin = crud.remove_admin(db, admin_id)
    if not remove_admin:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Admin not found",
            },
        )
    return ResponseModel(
        success=True,
        message="Admin deleted successfully",
    )


@router.patch("/admin/{admin_id}/status", response_model=ResponseModel)
async def toggle_admin_status(admin_id: int, db: Session = Depends(get_db)):
    status_changed = crud.change_admin_status(db, admin_id)
    if not status_changed:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Admin not found",
            },
        )
    return ResponseModel(
        success=True,
        message="Admin status changed successfully",
    )


@router.post("/panel", description="add a new panel", response_model=ResponseModel)
async def create_panel(panel_input: PanelInput, db: Session = Depends(get_db)):
    if crud.get_panel_by_name(db, panel_input.name):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "message": "Panel with this name already exists",
            },
        )

    connection = await create_new_panel(db, panel_input)
    if not connection:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": "Failed to connect to the panel with provided credentials",
            },
        )

    crud.add_panel(db, panel_input)
    return ResponseModel(
        success=True,
        message="Panel created successfully",
    )


@router.put("/panel/{panel_id}", response_model=ResponseModel)
async def update_panel(
    panel_id: int, panel_input: PanelInput, db: Session = Depends(get_db)
):
    if not crud.get_panel_by_id(db, panel_id):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Panel not found",
            },
        )
    connection = await update_a_panel(db, panel_input)
    if not connection:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": "Failed to connect to the panel with provided credentials",
            },
        )

    crud.update_panel_values(db, panel_id, panel_input)
    return ResponseModel(
        success=True,
        message="Panel updated successfully",
    )


@router.delete("/panel/{panel_id}", response_model=ResponseModel)
async def delete_panel(panel_id: int, db: Session = Depends(get_db)):
    remove_panel = crud.remove_panel(db, panel_id)
    if not remove_panel:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Panel not found",
            },
        )
    return ResponseModel(
        success=True,
        message="Panel deleted successfully",
    )


@router.patch("/panel/{panel_id}/status", response_model=ResponseModel)
async def toggle_panel_status(panel_id: int, db: Session = Depends(get_db)):
    status_changed = crud.change_panel_status(db, panel_id)
    if not status_changed:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Panel not found",
            },
        )
    return ResponseModel(
        success=True,
        message="Panel status changed successfully",
    )
