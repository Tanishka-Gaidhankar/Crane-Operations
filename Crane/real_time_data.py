# real_time_data.py - Simulate Real-Time Crane Sensor Data
import pandas as pd
import numpy as np
import time
import requests
from datetime import datetime

# Define API endpoint (Flask backend)
API_URL = "http://127.0.0.1:5000/predict"

# Function to simulate real-time crane data
def generate_real_time_data():
    return {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Load_Weight": round(np.random.uniform(500, 5000), 2),
        "Motor_Temperature": round(np.random.uniform(30, 90), 2),
        "Vibration_Level": round(np.random.uniform(0.2, 5.0), 2),
        "Operating_Hours": round(np.random.uniform(100, 3000), 2),
    }

# Send real-time data to API
while True:
    data = generate_real_time_data()
    response = requests.post(API_URL, json=data)
    print(f"Sent Data: {data}, Response: {response.json()}")
    time.sleep(5)  # Send data every 5 seconds
