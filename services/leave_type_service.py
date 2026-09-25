from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.leave_type import LeaveType


def create_leave_type(db: Session, data):

    existing = db.query(LeaveType).filter(
        LeaveType.leave_name == data.leave_name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Leave type already exists"
        )

    if data.total_days <= 0:
        raise HTTPException(
            status_code=400,
            detail="Total days must be greater than 0"
        )

    leave_type = LeaveType(
        leave_name=data.leave_name,
        total_days=data.total_days,
        description=data.description
    )

    db.add(leave_type)

    try:
        db.commit()
        db.refresh(leave_type)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Leave type already exists"
        )

    return leave_type


def get_leave_types(db: Session):

    return db.query(LeaveType).all()


def get_leave_type(
    db: Session,
    leave_type_id: int
):

    return (
        db.query(LeaveType)
        .filter(
            LeaveType.id == leave_type_id
        )
        .first()
    )