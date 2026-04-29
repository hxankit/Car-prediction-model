from sqlalchemy.orm import Session
from app.models.car import Car
import pickle
import numpy as np
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../predictionModel/app"))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(os.path.join(BASE_DIR, "mappings", "brand_map.json")) as f:
    brand_map = json.load(f)
with open(os.path.join(BASE_DIR, "mappings", "model_map.json")) as f:
    model_map = json.load(f)

def create_Car_service(db: Session, car):
    carSetup = Car(
        name=car.name,
        brand=car.brand,
        year=car.year,
        price=car.price,
        fuel_type=car.fuel_type,
        transmission=car.transmission,
        kms_driven=car.kms_driven,
        owner_count=car.owner_count,
    )
    db.add(carSetup)
    db.commit()
    db.refresh(carSetup)
    return carSetup

def get_car_by_id(db: Session, car_id: str):
    return db.query(Car).filter(Car.id == car_id).first()

def predict_car_price(data):

    # Validation
    if data.brand not in brand_map:
        raise ValueError("Invalid brand")

    if data.model not in model_map:
        raise ValueError("Invalid model")

    brand_encoded = brand_map[data.brand]
    model_encoded = model_map[data.model]

    # One-hot encoding
    fuel = [
        1 if data.fuel == "CNG" else 0,
        1 if data.fuel == "Diesel" else 0,
        1 if data.fuel == "LPG" else 0,
        1 if data.fuel == "Petrol" else 0,
    ]

    seller = [
        1 if data.seller_type == "Dealer" else 0,
        1 if data.seller_type == "Individual" else 0,
        1 if data.seller_type == "Trustmark Dealer" else 0,
    ]

    transmission = [
        1 if data.transmission == "Automatic" else 0,
        1 if data.transmission == "Manual" else 0,
    ]

    input_data = np.array([[ 
        brand_encoded,
        model_encoded,
        data.year,
        data.km_driven,
        data.owner,
        data.mileage,
        data.engine,
        data.max_power,
        data.seats,
        *fuel,
        *seller,
        *transmission
    ]])

    prediction = model.predict(input_data)

    return {
        "predicted_price": round(float(prediction[0]), 2),
        "message":"The best price of your car"
    }

# def delete_user_service(db:Session,email:str):
#     user =db.query(User).filter(User.email==email).first
#     if not user:
#         return None
#     db.delete(user)
#     db.commit()
#     db.refresh(user)
#     return user