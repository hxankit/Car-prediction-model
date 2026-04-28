from fastapi import FastAPI
import pickle
import numpy as np
import os
app=FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "model", "model.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

@app.get("/")
def home():
    return {"message":"Ai api is running"}

@app.post("/predict")
def predict(year:int,km_driven:int,owner:int,mileage:int):
    data = np.array([[year, km_driven, owner,mileage  ]])
    prediction=model.predict(data)

    return {
        "predicted Price":float(prediction[0])
    }