from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import base


class Employee(base):
    __tablename__ = "employees"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    employee_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    salary = Column(
        Integer,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False,
        index=True
    )

    department = relationship(
        "Department",
        back_populates="employees"
    )

    leave_requests = relationship(
    "LeaveRequest",
    back_populates="employee"
)

    payrolls = relationship(
    "Payroll",
    back_populates="employee"
)