from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.payroll import Payroll
from models.employee import Employee


def create_payroll(
    db: Session,
    data
):

    employee = (
        db.query(Employee)
        .filter(Employee.id == data.employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    existing = (
        db.query(Payroll)
        .filter(
            Payroll.employee_id == data.employee_id,
            Payroll.month == data.month
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Payroll already exists for this employee and month"
        )

    net_salary = (
        data.basic_salary
        + data.allowances
        - data.deductions
    )

    payroll = Payroll(
        employee_id=data.employee_id,
        month=data.month,
        basic_salary=data.basic_salary,
        allowances=data.allowances,
        deductions=data.deductions,
        net_salary=net_salary
    )

    db.add(payroll)
    db.commit()
    db.refresh(payroll)

    return payroll


def get_payrolls(
    db: Session
):

    return (
        db.query(Payroll)
        .all()
    )


def get_employee_payrolls(
    db: Session,
    employee_id: int
):

    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return (
        db.query(Payroll)
        .filter(
            Payroll.employee_id == employee_id
        )
        .all()
    )


def get_payroll(
    db: Session,
    payroll_id: int
):

    payroll = (
        db.query(Payroll)
        .filter(
            Payroll.id == payroll_id
        )
        .first()
    )

    if payroll is None:
        raise HTTPException(
            status_code=404,
            detail="Payroll not found"
        )

    return payroll


def update_payroll(
    db: Session,
    payroll_id: int,
    data
):

    payroll = (
        db.query(Payroll)
        .filter(
            Payroll.id == payroll_id
        )
        .first()
    )

    if payroll is None:
        raise HTTPException(
            status_code=404,
            detail="Payroll not found"
        )

    if data.basic_salary is not None:
        payroll.basic_salary = data.basic_salary

    if data.allowances is not None:
        payroll.allowances = data.allowances

    if data.deductions is not None:
        payroll.deductions = data.deductions

    payroll.net_salary = (
        payroll.basic_salary
        + payroll.allowances
        - payroll.deductions
    )

    db.commit()
    db.refresh(payroll)

    return payroll


def delete_payroll(
    db: Session,
    payroll_id: int
):

    payroll = (
        db.query(Payroll)
        .filter(
            Payroll.id == payroll_id
        )
        .first()
    )

    if payroll is None:
        raise HTTPException(
            status_code=404,
            detail="Payroll not found"
        )

    db.delete(payroll)
    db.commit()

    return {
        "message": "Payroll deleted successfully"
    }

