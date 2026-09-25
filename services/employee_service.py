from math import ceil

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.employee import Employee
from models.department import Department


def create_employee(db: Session, data):

    department = db.query(Department).filter(
        Department.id == data.department_id
    ).first()

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    employee = Employee(
        employee_id=data.employee_id,
        name=data.name,
        email=data.email,
        salary=data.salary,
        department_id=data.department_id,
        is_active=data.is_active
    )

    db.add(employee)

    try:
        db.commit()
        db.refresh(employee)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Employee ID or email already exists"
        )

    return employee


def get_employee(db: Session, employee_id: int):

    return (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )


def get_employees(
    db: Session,
    department_id=None,
    status=None,
    search=None,
    page=1,
    limit=10,
    sort_by="id",
    order="asc"
):

    if page < 1:
        page = 1

    if limit < 1:
        limit = 10

    if limit > 100:
        limit = 100

    query = db.query(Employee)

    if department_id is not None:
        query = query.filter(
            Employee.department_id == department_id
        )

    if status is not None:

        status = status.lower()

        if status == "active":
            query = query.filter(
                Employee.is_active == True
            )

        elif status == "inactive":
            query = query.filter(
                Employee.is_active == False
            )

    if search:

        search_value = f"%{search}%"

        query = query.filter(
            (Employee.name.ilike(search_value)) |
            (Employee.employee_id.ilike(search_value)) |
            (Employee.email.ilike(search_value))
        )

    sort_columns = {
        "id": Employee.id,
        "employee_id": Employee.employee_id,
        "name": Employee.name,
        "email": Employee.email,
        "salary": Employee.salary,
        "department_id": Employee.department_id,
        "is_active": Employee.is_active
    }

    sort_column = sort_columns.get(
        sort_by,
        Employee.id
    )

    if order.lower() == "desc":
        query = query.order_by(
            sort_column.desc()
        )
    else:
        query = query.order_by(
            sort_column.asc()
        )

    total = query.count()

    offset = (page - 1) * limit

    employees = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    pages = ceil(total / limit) if total else 0

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages,
        "data": employees
    }


def create_department(db: Session, data):

    existing = db.query(Department).filter(
        Department.name == data.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Department already exists"
        )

    department = Department(
        name=data.name,
        description=data.description
    )

    db.add(department)

    try:
        db.commit()
        db.refresh(department)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Department already exists"
        )

    return department


def get_departments(db: Session):

    return db.query(Department).all()


def get_department(
    db: Session,
    department_id: int
):

    return (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
    )


def get_department_employees(
    db: Session,
    department_id: int
):

    return (
        db.query(Employee)
        .filter(
            Employee.department_id == department_id
        )
        .all()
    )