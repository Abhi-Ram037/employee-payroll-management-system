from pydantic import BaseModel, ConfigDict


class LeaveTypeCreate(BaseModel):
    leave_name: str
    total_days: int
    description: str | None = None


class LeaveTypeResponse(BaseModel):
    id: int
    leave_name: str
    total_days: int
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)