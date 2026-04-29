from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password

def create_user_service(db: Session, user):
    db_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_service(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def delete_user_service(db:Session,email:str):
    user =db.query(User).filter(User.email==email).first
    if not user:
        return None
    db.delete(user)
    db.commit()
    db.refresh(user)
    return user