from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from services.auth_service import check_role


router = APIRouter(
    prefix="/rbac",
    tags=["RBAC"]
)


@router.get("/admin")
def admin_access(
    username: str,
    db: Session = Depends(get_db)
):

    return check_role(
        db,
        username,
        ["admin"]
    )


@router.get("/manager")
def manager_access(
    username: str,
    db: Session = Depends(get_db)
):

    return check_role(
        db,
        username,
        ["admin", "manager"]
    )


@router.get("/employee")
def employee_access(
    username: str,
    db: Session = Depends(get_db)
):

    return check_role(
        db,
        username,
        ["admin", "manager", "employee"]
    )