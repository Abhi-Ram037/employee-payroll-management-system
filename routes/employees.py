from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.employee import EmployeeCreate, EmployeeResponse
from schemas.pagination import PaginatedResponse
from services.employee_service import (
    create_employee,
    get_employees,
    get_employee
)
from services.auth_service import check_role


router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.post(
    "",
    response_model=EmployeeResponse
)
def add_employee(
    username: str,
    data: EmployeeCreate,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin", "manager"]
    )

    return create_employee(
        db,
        data
    )


@router.get(
    "",
    response_model=PaginatedResponse[EmployeeResponse]
)
def employee_list(
    username: str,
    department_id: int | None = None,
    status: str | None = None,
    search: str | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin", "manager"]
    )

    return get_employees(
        db,
        department_id=department_id,
        status=status,
        search=search,
        page=page,
        limit=limit,
        sort_by=sort_by,
        order=order
    )


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def employee_details(
    employee_id: int,
    username: str,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin", "manager", "employee"]
    )

    employee = get_employee(
        db,
        employee_id
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee