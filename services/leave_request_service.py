from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.leave_request import LeaveRequest
from models.employee import Employee
from models.leave_type import LeaveType


def create_leave_request(db: Session, data):

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

    if not employee.is_active:
        raise HTTPException(
            status_code=400,
            detail="Inactive employee cannot apply for leave"
        )

    leave_type = (
        db.query(LeaveType)
        .filter(LeaveType.id == data.leave_type_id)
        .first()
    )

    if leave_type is None:
        raise HTTPException(
            status_code=404,
            detail="Leave type not found"
        )

    if data.start_date > data.end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date"
        )

    existing = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.employee_id == data.employee_id,
            LeaveRequest.start_date <= data.end_date,
            LeaveRequest.end_date >= data.start_date
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Leave dates overlap with an existing request"
        )

    duration = (
        data.end_date - data.start_date
    ).days + 1

    if duration <= 0:
        raise HTTPException(
            status_code=400,
            detail="Leave days must be greater than 0"
        )

    leave_request = LeaveRequest(
        employee_id=data.employee_id,
        leave_type_id=data.leave_type_id,
        start_date=data.start_date,
        end_date=data.end_date,
        reason=data.reason,
        status="pending",
        duration=duration
    )

    db.add(leave_request)
    db.commit()
    db.refresh(leave_request)

    return leave_request


def get_leave_requests(
    db: Session,
    status=None,
    employee_id=None,
    start_date=None,
    end_date=None,
    page=1,
    limit=10,
    sort_by="id",
    order="asc"
):

    query = db.query(LeaveRequest)

    if status:
        query = query.filter(
            LeaveRequest.status == status.lower()
        )

    if employee_id:
        query = query.filter(
            LeaveRequest.employee_id == employee_id
        )

    if start_date:
        query = query.filter(
            LeaveRequest.start_date >= start_date
        )

    if end_date:
        query = query.filter(
            LeaveRequest.end_date <= end_date
        )

    allowed_sort_fields = {
        "id": LeaveRequest.id,
        "employee_id": LeaveRequest.employee_id,
        "leave_type_id": LeaveRequest.leave_type_id,
        "start_date": LeaveRequest.start_date,
        "end_date": LeaveRequest.end_date,
        "status": LeaveRequest.status,
        "duration": LeaveRequest.duration
    }

    sort_column = allowed_sort_fields.get(
        sort_by,
        LeaveRequest.id
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

    if page < 1:
        page = 1

    if limit < 1:
        limit = 10

    offset = (page - 1) * limit

    data = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages,
        "data": data
    }


def get_leave_request(
    db: Session,
    leave_request_id: int
):

    return (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.id == leave_request_id
        )
        .first()
    )


def update_leave_status(
    db: Session,
    leave_request_id: int,
    status: str
):

    leave_request = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.id == leave_request_id
        )
        .first()
    )

    if leave_request is None:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found"
        )

    status = status.lower()

    if status not in [
        "pending",
        "approved",
        "rejected"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    if leave_request.status == "approved":
        if status == "approved":
            raise HTTPException(
                status_code=400,
                detail="Leave is already approved"
            )

        if status == "pending":
            raise HTTPException(
                status_code=400,
                detail="Approved leave cannot be changed to pending"
            )

    if leave_request.status == "rejected":
        if status == "approved":
            raise HTTPException(
                status_code=400,
                detail="Rejected leave cannot be approved later"
            )

        if status == "rejected":
            raise HTTPException(
                status_code=400,
                detail="Leave is already rejected"
            )

    if leave_request.status == "pending":
        if status == "pending":
            raise HTTPException(
                status_code=400,
                detail="Leave is already pending"
            )

    leave_request.status = status

    db.commit()
    db.refresh(leave_request)

    return leave_request


def delete_leave_request(
    db: Session,
    leave_request_id: int
):

    leave_request = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.id == leave_request_id
        )
        .first()
    )

    if leave_request is None:
        raise HTTPException(
            status_code=404,
            detail="Leave request not found"
        )

    db.delete(leave_request)
    db.commit()

    return {
        "message": "Leave request deleted successfully"
    }

def get_leave_balance(
    db: Session,
    employee_id: int,
    leave_type_id: int
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

    leave_type = (
        db.query(LeaveType)
        .filter(LeaveType.id == leave_type_id)
        .first()
    )

    if leave_type is None:
        raise HTTPException(
            status_code=404,
            detail="Leave type not found"
        )

    approved_leaves = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.employee_id == employee_id,
            LeaveRequest.leave_type_id == leave_type_id,
            LeaveRequest.status == "approved"
        )
        .all()
    )

    used_days = sum(
        leave.duration
        for leave in approved_leaves
    )

    remaining_days = (
        leave_type.total_days - used_days
    )

    if remaining_days < 0:
        remaining_days = 0

    return {
        "employee_id": employee.id,
        "employee_name": employee.name,
        "leave_type_id": leave_type.id,
        "leave_type": leave_type.leave_name,
        "total_days": leave_type.total_days,
        "used_days": used_days,
        "remaining_days": remaining_days
    }