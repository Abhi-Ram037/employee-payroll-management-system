from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.department import Department
from models.employee import Employee


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
    db.commit()
    db.refresh(department)

    return department


def get_departments(db: Session):
    return db.query(Department).all()


def get_department(
    db: Session,
    department_id: int
):
    return db.query(Department).filter(
        Department.id == department_id
    ).first()


def get_department_employees(
    db: Session,
    department_id: int
):
    return db.query(Employee).filter(
        Employee.department_id == department_id
    ).all()

def get_department_employees(
    db: Session,
    department_id: int
):
    department = (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
    )

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return (
        db.query(Employee)
        .filter(Employee.department_id == department_id)
        .all()
    )