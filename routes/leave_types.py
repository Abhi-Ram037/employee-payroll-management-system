from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.leave_type import LeaveTypeCreate, LeaveTypeResponse
from services.leave_type_service import (
    create_leave_type,
    get_leave_types,
    get_leave_type
)


router = APIRouter(
    prefix="/leave-types",
    tags=["Leave Types"]
)


@router.post(
    "",
    response_model=LeaveTypeResponse
)
def add_leave_type(
    data: LeaveTypeCreate,
    db: Session = Depends(get_db)
):
    return create_leave_type(db, data)


@router.get(
    "",
    response_model=list[LeaveTypeResponse]
)
def leave_type_list(
    db: Session = Depends(get_db)
):
    return get_leave_types(db)


@router.get(
    "/{leave_type_id}",
    response_model=LeaveTypeResponse
)
def leave_type_details(
    leave_type_id: int,
    db: Session = Depends(get_db)
):
    leave_type = get_leave_type(
        db,
        leave_type_id
    )

    if leave_type is None:
        raise HTTPException(
            status_code=404,
            detail="Leave type not found"
        )

    return leave_type