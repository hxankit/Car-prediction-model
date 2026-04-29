from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.core.database import get_db
from app.controllers.userController import (
    register_user,
    login_user,
    delete_user_controller
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user)


@router.delete("/{email}")
def delete_user(email: str, db: Session = Depends(get_db)):
    return delete_user_controller(db, email)