from fastapi import HTTPException
from app.services.userServices import (
    create_user_service,
    get_user_service,
    delete_user_service,
)
from app.core.security import verify_password, create_token


def register_user(db, user):
    existing = get_user_service(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    create_user_service(db, user)
    return {"message":"Car created succesfully"}


def login_user(db, user):
    db_user = get_user_service(db, user.email)

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": db_user.email})
    return {"access_token": token}


def delete_user_controller(db, email: str):
    user = get_user_service(db, email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    delete_user_service(db, user)
    return {"message": "User deleted successfully"}