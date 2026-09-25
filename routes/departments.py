from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.department import DepartmentCreate, DepartmentResponse
from services.department_service import (
    create_department,
    get_departments,
    get_department,
    get_department_employees
)
from schemas.employee import (
    EmployeeCreate,
    EmployeeResponse
)
from services.auth_service import check_role


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post(
    "",
    response_model=DepartmentResponse
)
def add_department(
    username: str,
    data: DepartmentCreate,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin"]
    )

    return create_department(
        db,
        data
    )


@router.get(
    "",
    response_model=list[DepartmentResponse]
)
def department_list(
    username: str,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin", "manager"]
    )

    return get_departments(db)


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse
)
def department_details(
    department_id: int,
    username: str,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin", "manager", "employee"]
    )

    department = get_department(
        db,
        department_id
    )

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department


@router.get(
    "/{department_id}/employees",
    response_model=list[EmployeeResponse]
)
def department_employees(
    department_id: int,
    username: str,
    db: Session = Depends(get_db)
):

    check_role(
        db,
        username,
        ["admin", "manager"]
    )

    return get_department_employees(
        db,
        department_id
    )