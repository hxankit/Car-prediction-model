from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
import os
import json

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
# Load model
with open(os.path.join(BASE_DIR, "app/model/model.pkl"), "rb") as f:
    model = pickle.load(f)

# Load mappings
with open(os.path.join(BASE_DIR, "app/mappings/brand_map.json")) as f:
    brand_map = json.load(f)

with open(os.path.join(BASE_DIR, "app/mappings/model_map.json")) as f:
    model_map = json.load(f)


# Input schema
class CarInput(BaseModel):
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


@app.get("/")
def home():
    return {"message": "AI Car Price API Running 🚀"}


@app.post("/predict")
def predict(data: CarInput):

    # ✅ Validate + encode
    if data.brand not in brand_map:
        raise HTTPException(status_code=400, detail="Invalid brand")

    if data.model not in model_map:
        raise HTTPException(status_code=400, detail="Invalid model")

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

    # ⚠️ Order MUST match training
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
        "predicted_price": float(prediction[0])
    }