# Database models for User
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    role=Column(String(20), default="user")
    isVerified=Column(String(20),default="notVerified")
    verificationToken=Column(String(50))