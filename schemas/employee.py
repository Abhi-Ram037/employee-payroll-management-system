from pydantic import BaseModel, ConfigDict


class EmployeeCreate(BaseModel):
    employee_id: str
    name: str
    email: str
    salary: int
    department_id: int
    is_active: bool = True


class EmployeeResponse(BaseModel):
    id: int
    employee_id: str
    name: str
    email: str
    salary: int
    department_id: int
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class EmployeeListResponse(BaseModel):
    page: int
    limit: int
    total: int
    pages: int
    data: list[EmployeeResponse]