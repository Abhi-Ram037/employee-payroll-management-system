from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.user import User


def get_user_by_username(
    db: Session,
    username: str
):
    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )


def check_role(
    db: Session,
    username: str,
    allowed_roles: list[str]
):
    user = get_user_by_username(
        db,
        username
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    if user.role not in allowed_roles:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission"
        )

    return user