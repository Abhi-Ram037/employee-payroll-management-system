from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import base


class LeaveRequest(base):
    __tablename__ = "leave_requests"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False,
        index=True
    )

    leave_type_id = Column(
        Integer,
        ForeignKey("leave_types.id"),
        nullable=False,
        index=True
    )

    start_date = Column(
        Date,
        nullable=False
    )

    end_date = Column(
        Date,
        nullable=False
    )

    reason = Column(
        String(255),
        nullable=True
    )

    duration = Column(
        Integer,
        nullable=False
    )

    status = Column(
        String(20),
        default="pending",
        nullable=False
    )

    employee = relationship(
        "Employee",
        back_populates="leave_requests"
    )

    leave_type = relationship(
        "LeaveType",
        back_populates="leave_requests"
    )