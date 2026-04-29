import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "../Data/car_cleaned_with_model.csv")

df = pd.read_csv(data_path)
df = df.dropna()

# ✅ Generate mappings dynamically
brand_map = dict(zip(df["brand"], df["brand_encoded"]))
model_map = dict(zip(df["model"], df["model_encoded"]))

# Save mappings
mapping_dir = os.path.join(BASE_DIR, "../app/mappings")
os.makedirs(mapping_dir, exist_ok=True)

with open(os.path.join(mapping_dir, "brand_map.json"), "w") as f:
    json.dump(brand_map, f)

with open(os.path.join(mapping_dir, "model_map.json"), "w") as f:
    json.dump(model_map, f)

# ❌ Drop raw columns
df = df.drop(["brand", "model"], axis=1)

# Features & target
X = df.drop("selling_price", axis=1)
y = df["selling_price"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
model_dir = os.path.join(BASE_DIR, "../app/model")
os.makedirs(model_dir, exist_ok=True)

with open(os.path.join(model_dir, "model.pkl"), "wb") as f:
    pickle.dump(model, f)

print("✅ Model + mappings saved successfully")