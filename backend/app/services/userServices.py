from sqlalchemy.orm import Session
from app.models.user import User
import secrets
import string
from app.core.security import hash_password
def generate_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

def generate_token():
    return secrets.token_urlsafe(32)

def create_user_service(db: Session, user):
    raw_password = generate_password()
    token = generate_token()

    db_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(raw_password),
        isVerified=False,
        verificationToken=token
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "user": db_user,
        "password": raw_password,
        "token": token
    }
def get_user_service(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
def get_user_by_token(db: Session, token: str):
    return db.query(User).filter(User.verificationToken == token).first()


def delete_user_service(db:Session,email:str):
    user =db.query(User).filter(User.email==email).first
    if not user:
        return None
    db.delete(user)
    db.commit()
    db.refresh(user)
    return user