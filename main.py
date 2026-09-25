from fastapi import FastAPI

from database import base, engine

from routes import employees
from routes import departments
from routes import leave_types
from routes import leave_requests
from routes import payrolls
from routes import auth
from routes import rbac


base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Employee Payroll Management System",
    version="0.1.0"
)


@app.get("/")
def home():
    return {
        "message": "Employee Payroll Management System"
    }


app.include_router(employees.router)
app.include_router(departments.router)
app.include_router(leave_types.router)
app.include_router(leave_requests.router)
app.include_router(payrolls.router)
app.include_router(auth.router)
app.include_router(rbac.router)