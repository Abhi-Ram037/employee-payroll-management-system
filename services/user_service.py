from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.user import User


def create_user(db: Session, data):

    existing = (
        db.query(User)
        .filter(User.username == data.username)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    if data.role not in ["admin", "manager", "employee"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    user = User(
        username=data.username,
        password=data.password,
        role=data.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(
    db: Session,
    username: str,
    password: str
):

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if user.password != password:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return user