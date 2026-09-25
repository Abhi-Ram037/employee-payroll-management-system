from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import base


class LeaveType(base):
    __tablename__ = "leave_types"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    leave_name = Column(
        String(100),
        unique=True,
        nullable=False
    )

    total_days = Column(
        Integer,
        nullable=False
    )

    description = Column(
        String(255),
        nullable=True
    )

    leave_requests = relationship(
        "LeaveRequest",
        back_populates="leave_type"
    )