from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from schemas.payroll import (
    PayrollCreate,
    PayrollUpdate,
    PayrollResponse
)

from services.payroll_service import (
    create_payroll,
    get_payrolls,
    get_employee_payrolls,
    get_payroll,
    update_payroll,
    delete_payroll
)

from services.auth_service import check_role


router = APIRouter(
    prefix="/payrolls",
    tags=["Payrolls"]
)


@router.post(
    "",
    response_model=PayrollResponse
)
def add_payroll(
    username: str,
    data: PayrollCreate,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin"]
    )

    return create_payroll(
        db,
        data
    )


@router.get(
    "",
    response_model=list[PayrollResponse]
)
def payroll_list(
    username: str,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin", "manager"]
    )

    return get_payrolls(db)


@router.get(
    "/employee/{employee_id}",
    response_model=list[PayrollResponse]
)
def employee_payroll_list(
    employee_id: int,
    username: str,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin", "manager", "employee"]
    )

    return get_employee_payrolls(
        db,
        employee_id
    )


@router.get(
    "/{payroll_id}",
    response_model=PayrollResponse
)
def payroll_details(
    payroll_id: int,
    username: str,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin", "manager", "employee"]
    )

    return get_payroll(
        db,
        payroll_id
    )


@router.put(
    "/{payroll_id}",
    response_model=PayrollResponse
)
def edit_payroll(
    payroll_id: int,
    username: str,
    data: PayrollUpdate,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin"]
    )

    return update_payroll(
        db,
        payroll_id,
        data
    )


@router.delete(
    "/{payroll_id}"
)
def remove_payroll(
    payroll_id: int,
    username: str,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin"]
    )

    return delete_payroll(
        db,
        payroll_id
    )
