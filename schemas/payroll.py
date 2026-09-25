from pydantic import BaseModel
from typing import Optional


class PayrollCreate(BaseModel):
    employee_id: int
    month: str
    basic_salary: float
    allowances: float
    deductions: float


class PayrollUpdate(BaseModel):
    basic_salary: Optional[float] = None
    allowances: Optional[float] = None
    deductions: Optional[float] = None


class PayrollResponse(BaseModel):
    id: int
    employee_id: int
    month: str
    basic_salary: float
    allowances: float
    deductions: float
    net_salary: float

    class Config:
        from_attributes = True

