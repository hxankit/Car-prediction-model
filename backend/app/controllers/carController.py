from fastapi import HTTPException
from app.services.carServices import (
    create_Car_service,
    get_car_by_id,
    predict_car_price
    )

def createCar(db, car):
   
    return create_Car_service(db, car)

def get_car_controller(db, car_id):
    car = get_car_by_id(db, car_id)

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    # Example business logic (optional)
    if car.price is not None and car.price < 0:
        raise HTTPException(status_code=400, detail="Invalid car price")

    return car


def predict_car_price_controller(data):

    try:
        return predict_car_price(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

