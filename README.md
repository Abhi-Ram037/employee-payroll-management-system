# Employee Payroll Management System

## Overview

Employee Payroll Management System is a backend application developed using Python and FastAPI. The system manages employees, departments, leave types, leave requests, leave balances, and payroll information. It also includes authentication and Role-Based Access Control (RBAC) for Admin, Manager, and Employee users.

The project provides REST APIs that can be tested through FastAPI Swagger UI.

## Technologies Used

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Uvicorn
* REST API
* Swagger UI
* Git and GitHub

## Main Features

### Employee Management

* Add employee
* View employee list
* View employee details
* Filter employees by department and status
* Search employees
* Pagination
* Sorting

### Department Management

* Add department
* View department list
* View department details
* View employees belonging to a department

### Leave Type Management

* Add leave type
* View leave type list
* View leave type details

### Leave Request Management

* Create leave request
* View leave requests
* View individual leave request
* Update leave request status
* Delete leave request
* Prevent inactive employees from applying for leave
* Prevent overlapping leave requests
* Automatically calculate leave duration
* Filter leave requests
* Pagination
* Sorting

### Leave Balance

The system provides leave balance information for an employee based on the selected leave type.

It displays:

* Total leave days
* Used leave days
* Remaining leave days

### Payroll Management

* Add payroll
* View all payroll records
* View payroll records for an employee
* View payroll details
* Edit payroll
* Delete payroll
* Automatically calculate net salary
* Prevent duplicate payroll records for the same employee and month

### Authentication

The project includes:

* User registration
* User login

### Role-Based Access Control

The system supports three roles:

* Admin
* Manager
* Employee

Different operations are restricted according to the user's role.

## Project Structure

```text
employee_payroll_management_system/
│
├── main.py
├── database.py
│
├── models/
│   ├── employee.py
│   ├── department.py
│   ├── leave_type.py
│   ├── leave_request.py
│   ├── payroll.py
│   └── user.py
│
├── schemas/
│   ├── employee.py
│   ├── department.py
│   ├── leave_type.py
│   ├── leave_request.py
│   ├── payroll.py
│   └── user.py
│
├── services/
│   ├── employee_service.py
│   ├── department_service.py
│   ├── leave_type_service.py
│   ├── leave_request_service.py
│   ├── payroll_service.py
│   └── auth_service.py
│
├── routes/
│   ├── employees.py
│   ├── departments.py
│   ├── leave_types.py
│   ├── leave_requests.py
│   ├── payrolls.py
│   ├── auth.py
│   └── rbac.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

## API Modules

### Employees

```text
POST   /employees
GET    /employees
GET    /employees/{employee_id}
```

### Departments

```text
POST   /departments
GET    /departments
GET    /departments/{department_id}
GET    /departments/{department_id}/employees
```

### Leave Types

```text
GET    /leave-types
POST   /leave-types
GET    /leave-types/{leave_type_id}
```

### Leave Requests

```text
POST   /leave-requests
GET    /leave-requests
GET    /leave-requests/{leave_request_id}
DELETE /leave-requests/{leave_request_id}
PATCH  /leave-requests/{leave_request_id}/status
GET    /leave-requests/balance/{employee_id}
```

### Payrolls

```text
POST   /payrolls
GET    /payrolls
GET    /payrolls/employee/{employee_id}
GET    /payrolls/{payroll_id}
PUT    /payrolls/{payroll_id}
DELETE /payrolls/{payroll_id}
```

### Authentication

```text
POST   /auth/register
POST   /auth/login
```

### RBAC

```text
GET    /rbac/admin
GET    /rbac/manager
GET    /rbac/employee
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Abhi-Ram037/employee-payroll-management-system.git
```

Move into the project folder:

```bash
cd employee-payroll-management-system
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run the Application

Start the FastAPI application using:

```bash
python -m uvicorn main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

## Swagger Documentation

After starting the application, open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test all available API endpoints.

## Database

The project uses SQLAlchemy for database operations. SQLite is used as the database for storing employee, department, leave, payroll, and user information.

## Payroll Calculation

The net salary is calculated using:

```text
net salary = basic salary + allowances - deductions
```

For example:

```text
Basic Salary = 35000
Allowances   = 5000
Deductions   = 2000

Net Salary = 35000 + 5000 - 2000
           = 38000
```

## Leave Duration Calculation

Leave duration is calculated automatically based on the start date and end date.

```text
duration = (end date - start date) + 1
```

For example:

```text
Start Date = 2026-09-25
End Date   = 2026-09-27

Duration = 3 days
```

## Validation and Business Rules

The application includes several validations:

* Employee must exist before creating a leave request.
* Inactive employees cannot apply for leave.
* Leave type must exist.
* Start date cannot be after end date.
* Overlapping leave requests are prevented.
* Leave duration is calculated automatically.
* Payroll cannot be duplicated for the same employee and month.
* Payroll net salary is calculated automatically.
* Only authorized roles can perform restricted operations.

## Testing

The APIs can be tested using:

* FastAPI Swagger UI
* Browser
* Postman
* cURL

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## GitHub

Repository:

```text
https://github.com/Abhi-Ram037/employee-payroll-management-system
```

## Project Purpose

This project was developed to practice backend development using Python and FastAPI. It demonstrates CRUD operations, database integration, API validation, business logic, authentication, role-based access control, pagination, filtering, sorting, and REST API development.

## Author

Abhiram
