from pydantic import BaseModel
from datetime import date


class LeaveRequestCreate(BaseModel):
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    reason: str


class LeaveRequestResponse(BaseModel):
    id: int
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    reason: str
    status: str
    duration: int

    class Config:
        from_attributes = True


class LeaveRequestStatusUpdate(BaseModel):
    status: str


class LeaveBalanceResponse(BaseModel):
    employee_id: int
    employee_name: str
    leave_type_id: int
    leave_type: str
    total_days: int
    used_days: int
    remaining_days: int


class LeaveRequestPage(BaseModel):
    page: int
    limit: int
    total: int
    pages: int
    data: list[LeaveRequestResponse]