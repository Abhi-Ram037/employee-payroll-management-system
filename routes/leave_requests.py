from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from schemas.leave_request import (
    LeaveRequestCreate,
    LeaveRequestResponse,
    LeaveRequestStatusUpdate,
    LeaveRequestPage,
    LeaveBalanceResponse
)

from services.leave_request_service import (
    create_leave_request,
    get_leave_requests,
    get_leave_request,
    update_leave_status,
    delete_leave_request,
    get_leave_balance
)

from services.auth_service import check_role


router = APIRouter(
    prefix="/leave-requests",
    tags=["Leave Requests"]
)


@router.post(
    "",
    response_model=LeaveRequestResponse
)
def add_leave_request(
    username: str,
    data: LeaveRequestCreate,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin", "manager", "employee"]
    )

    return create_leave_request(
        db,
        data
    )


@router.get(
    "",
    response_model=LeaveRequestPage
)
def leave_request_list(
    username: str,
    status: str | None = None,
    employee_id: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin", "manager", "employee"]
    )

    return get_leave_requests(
        db=db,
        status=status,
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        page=page,
        limit=limit,
        sort_by=sort_by,
        order=order
    )

@router.get(
    "/{leave_request_id}",
    response_model=LeaveRequestResponse
)

@router.get(
    "/balance/{employee_id}",
    response_model=LeaveBalanceResponse
)
def leave_balance(
    employee_id: int,
    leave_type_id: int,
    username: str,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin", "manager", "employee"]
    )

    return get_leave_balance(
        db,
        employee_id,
        leave_type_id
    )


@router.get(
    "/{leave_request_id}",
    response_model=LeaveRequestResponse
)
def leave_request_details(
    leave_request_id: int,
    username: str,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin", "manager", "employee"]
    )

    leave_request = get_leave_request(
        db,
        leave_request_id
    )

    if leave_request is None:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found"
        )

    return leave_request


@router.patch(
    "/{leave_request_id}/status",
    response_model=LeaveRequestResponse
)
def update_status(
    leave_request_id: int,
    username: str,
    data: LeaveRequestStatusUpdate,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin", "manager"]
    )

    return update_leave_status(
        db,
        leave_request_id,
        data.status
    )


@router.delete(
    "/{leave_request_id}"
)
def remove_leave_request(
    leave_request_id: int,
    username: str,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin"]
    )

    return delete_leave_request(
        db,
        leave_request_id
    )
