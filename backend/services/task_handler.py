from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse

from .sanaei import AdminTaskService
from backend.schema.output import ResponseModel
from backend.schema._input import PanelInput, ClientInput, ClientUpdateInput
from backend.services.sanaei import APIService
from backend.db import crud
from backend.utils.logger import logger


async def create_new_panel(db: Session, panel_input: PanelInput) -> bool:
    if panel_input.panel_type == "3x-ui":
        try:
            connection = await APIService(
                panel_input.url, panel_input.username, panel_input.password
            ).test_connection()

            if connection is None or not connection.cpu:
                logger.warning(
                    f"Panel validation failed: {panel_input.name} - missing required fields"
                )
                return False

            logger.info(f"Panel validated successfully: {panel_input.name}")
            return True
        except Exception as e:
            logger.error(f"Error connecting to panel {panel_input.url}: {str(e)}")
            return False


async def update_a_panel(db: Session, panel_input: PanelInput) -> bool:
    if panel_input.panel_type == "3x-ui":
        try:
            connection = await APIService(
                panel_input.url, panel_input.username, panel_input.password
            ).test_connection()

            if connection is None or not connection.cpu:
                logger.warning(
                    f"Panel validation failed during update: {panel_input.name} - missing required fields"
                )
                return False

            logger.info(
                f"Panel validated successfully during update: {panel_input.name}"
            )
            return True
        except Exception as e:
            logger.error(
                f"Error connecting to panel {panel_input.url} during update: {str(e)}"
            )
            return False


async def get_all_users_from_panel(admin_username: str, db: Session) -> JSONResponse:
    """This function retrieves all users from the panel associated with the given admin."""

    _admin = crud.get_admin_by_username(db, admin_username)
    panel = crud.get_panel_by_name(db, _admin.panel)

    if panel.panel_type == "3x-ui":
        admin_task = AdminTaskService(admin_username=admin_username, db=db)
        clients = await admin_task.get_all_users()

        if clients is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "message": "No users found",
                },
            )
        return ResponseModel(
            success=True,
            message="Users retrieved successfully",
            data=clients,
        )


async def add_new_user(
    admin_username: str, user_input: ClientInput, db: Session
) -> JSONResponse:
    """This function adds a new user to the panel associated with the given admin."""

    _admin = crud.get_admin_by_username(db, admin_username)
    panel = crud.get_panel_by_name(db, _admin.panel)

    if panel.panel_type == "3x-ui":

        admin_task = AdminTaskService(admin_username=admin_username, db=db)
        check_duplicate = await admin_task.get_client_by_email(user_input.email)

        if check_duplicate:
            logger.warning(
                f"Attempt to add user with duplicate email: {user_input.email} by admin: {admin_username}"
            )
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "success": False,
                    "message": "This email is reserved by another admins",
                },
            )

        success = await admin_task.add_client_to_panel(user_input)

        if not success:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "message": f"{success}",
                },
            )
        return ResponseModel(
            success=True,
            message="User added successfully",
        )


async def update_a_user(
    admin_username: str, uuid: str, user_input: ClientUpdateInput, db: Session
) -> bool:
    """This function updates an existing user in the panel associated with the given admin."""

    _admin = crud.get_admin_by_username(db, admin_username)
    panel = crud.get_panel_by_name(db, _admin.panel)

    if panel.panel_type == "3x-ui":

        admin_task = AdminTaskService(admin_username=admin_username, db=db)
        update_user = await admin_task.update_client_in_panel(uuid, user_input)

        if not update_user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "message": "Failed to update user",
                },
            )

        return ResponseModel(
            success=True,
            message="User updated successfully",
        )


async def delete_a_user(admin_username: str, uuid: str, db: Session) -> bool:
    """This function deletes a user from the panel associated with the given admin."""

    _admin = crud.get_admin_by_username(db, admin_username)
    panel = crud.get_panel_by_name(db, _admin.panel)

    if panel.panel_type == "3x-ui":

        admin_task = AdminTaskService(admin_username=admin_username, db=db)
        delete_user = await admin_task.delete_client_from_panel(uuid)

        if not delete_user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "message": "Failed to delete user",
                },
            )

        return ResponseModel(
            success=True,
            message="User deleted successfully",
        )
