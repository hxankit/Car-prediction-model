from sqlalchemy import Column, Integer, String, Float, ForeignKey

from app.core.database import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(100), nullable=False)
    brand = Column(String(100))
    year = Column(Integer)
    price = Column(Float)
    fuel_type = Column(String(50))        # Petrol / Diesel / EV
    transmission = Column(String(50))     # Manual / Automatic
    kms_driven = Column(Integer)
    owner_count=Column(Integer)