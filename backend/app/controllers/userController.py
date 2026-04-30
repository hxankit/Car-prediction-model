from fastapi import HTTPException

from app.services.userServices import (
    create_user_service,
    get_user_service,
    delete_user_service,
    get_user_by_token
)
from app.core.security import verify_password, create_token
from app.core.helpers.mailer import send_email


async def register_user(db, user):
    existing = get_user_service(db, user.email)

    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    res = create_user_service(db, user)

    if res:
        await send_email(
            to_email=user.email,
            subject="Account Created",
            body=f"""
Your account has been created.

Password: {res['password']}

Verify your account:
http://127.0.0.1:8000/auth/verify?token={res['token']}
"""
        )

    return {"message": "User created. Check email for password & verification."}
def login_user(db, user):
    db_user = get_user_service(db, user.email)

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": db_user.email})
    return {"access_token": token}

def verify_user(token, db):
    user = get_user_by_token(db,token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    user.isVerified = True
    user.verificationToken = None
    db.commit()
    return {"message": "Account verified successfully"}
def delete_user_controller(db, email: str):
    user = get_user_service(db, email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    delete_user_service(db, user)
    return {"message": "User deleted successfully"}