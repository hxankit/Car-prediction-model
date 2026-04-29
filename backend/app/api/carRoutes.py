from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.car import CarCreate ,CarPredictInput
from app.core.database import get_db
from app.controllers.carController import (
    createCar,
    get_car_controller,
    predict_car_price_controller
    )

router = APIRouter(prefix="/car", tags=["Car"])


@router.post("/register")
def create(car: CarCreate, db: Session = Depends(get_db)):
    return createCar(db,car)

@router.get("/{car_id}")
def get_car(car_id: str, db: Session = Depends(get_db)):
    return get_car_controller(db, car_id)



@router.post("/price/predict")
def predict(data: CarPredictInput):
    print("Working")
    return predict_car_price_controller(data)