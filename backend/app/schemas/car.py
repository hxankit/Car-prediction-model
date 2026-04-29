
from pydantic import BaseModel

class CarCreate(BaseModel):
    name: str
    brand: str
    year: int
    price: float
    fuel_type: str
    transmission: str
    kms_driven: int
    owner_count: int



class CarPredictInput(BaseModel):
    brand: str
    model: str
    year: int
    km_driven: int
    owner: int
    mileage: float
    engine: float
    max_power: float
    seats: float
    fuel: str
    seller_type: str
    transmission: str