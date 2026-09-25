from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from database import base


class Payroll(base):
    __tablename__ = "payrolls"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    month = Column(
        String(20),
        nullable=False
    )

    basic_salary = Column(
        Float,
        nullable=False
    )

    allowances = Column(
        Float,
        default=0
    )

    deductions = Column(
        Float,
        default=0
    )

    net_salary = Column(
        Float,
        nullable=False
    )

    employee = relationship(
        "Employee",
        back_populates="payrolls"
    )