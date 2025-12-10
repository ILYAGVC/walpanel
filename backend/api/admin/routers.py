from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


from backend.db.engin import get_db
from backend.auth import get_current_admin
from backend.schema.output import ResponseModel
from backend.schema._input import ClientInput, ClientUpdateInput
from backend.services.sanaei import AdminTaskService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/user", description="Get all users")
async def get_all_users(
    db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)
):
    if current_admin["role"] != "admin":
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Not authorized to access this resource."},
        )

    clients = await AdminTaskService(
        admin_username=current_admin["username"], db=db
    ).get_all_users()

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


@router.post("/user", description="Add a new user")
async def add_user(
    user_input: ClientInput,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    if current_admin["role"] != "admin":
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Not authorized to access this resource."},
        )

    admin_task = AdminTaskService(admin_username=current_admin["username"], db=db)
    check_duplicate = await admin_task.get_client_by_email(user_input.email)

    if check_duplicate:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "message": "This email is reserved by another admins",
            },
        )

    new_client = await admin_task.add_client_to_panel(user_input)

    if not new_client:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": f"{new_client}",
            },
        )
    return ResponseModel(
        success=True,
        message="User added successfully",
    )


@router.put("/user/{uuid}", description="Update an existing user")
async def update_user(
    uuid: str,
    user_input: ClientUpdateInput,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    if current_admin["role"] != "admin":
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Not authorized to access this resource."},
        )

    update_user = await AdminTaskService(
        admin_username=current_admin["username"], db=db
    ).update_client_in_panel(uuid, user_input)
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


@router.delete("/user/{uuid}", description="Delete a user")
async def delete_user(
    uuid: str,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    if current_admin["role"] != "admin":
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Not authorized to access this resource."},
        )

    delete_user = await AdminTaskService(
        admin_username=current_admin["username"], db=db
    ).delete_client_from_panel(uuid)
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
