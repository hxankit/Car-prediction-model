import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
import os
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "../../Data/car_cleaned.csv")
df = pd.read_csv(data_path)

df = df.dropna()

x = df.drop("selling_price", axis=1)
print(x.columns)
y = df["selling_price"]


model = LinearRegression()
model.fit(x, y)

with open("./backend/model/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved")