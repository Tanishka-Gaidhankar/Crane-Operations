from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)

# Load trained model & scaler
model = joblib.load("best_xgboost.pkl")  # Ensure this file exists
scaler = joblib.load("scaler.pkl")  # Ensure scaler file exists

# Feature Engineering Function
def process_input(data):
    df = pd.DataFrame([data])

    # Compute additional features
    df["Vibration_MA"] = df["Vibration_Level"].rolling(window=3, min_periods=1).mean()
    df["Temp_MA"] = df["Motor_Temperature"].rolling(window=3, min_periods=1).mean()

    # Standardize features
    features = ["Load_Weight", "Motor_Temperature", "Vibration_Level", "Operating_Hours", "Vibration_MA", "Temp_MA"]
    df[features] = scaler.transform(df[features])

    return df[features]

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    processed_data = process_input(data)

    # Make prediction
    prediction = model.predict(processed_data)[0]
    probability = model.predict_proba(processed_data)[0][1]  # Probability of failure

    response = {
        "Failure_Prediction": int(prediction),
        "Failure_Probability": round(probability, 2)
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
