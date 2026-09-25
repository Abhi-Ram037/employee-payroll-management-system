from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.user import UserCreate, UserResponse
from services.user_service import create_user, login_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, data)


@router.post(
    "/login",
    response_model=UserResponse
)
def login(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):
    return login_user(
        db,
        username,
        password
    )