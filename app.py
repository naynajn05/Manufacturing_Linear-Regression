import streamlit as st
import pickle
import json
import numpy as np

# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np

# Load model and scaler
with open("linear_regression_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("feature_columns.json", "r") as f:
    import json
    feature_columns = json.load(f)

# Define request schema
class InputData(BaseModel):
    Injection_Temperature: float
    Injection_Pressure: float
    Cycle_Time: float
    Cooling_Time: float
    Material_Viscosity: float
    Ambient_Temperature: float
    Machine_Age: float
    Operator_Experience: float
    Maintenance_Hours: float
    Temperature_Pressure_Ratio:float
    Total_Cycle_Time:float
    Efficiency_Score:float
    Machine_Utilization:float
        

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Manufacturing Output Prediction API!"}

@app.post("/predict")
def predict(data: InputData):
    try:
        input_dict = data.dict()
        input_df = [input_dict[col] for col in feature_columns]
        scaled_input = scaler.transform([input_df])
        prediction = model.predict(scaled_input)
        return {"Predicted_Output_Parts_Per_Hour": round(float(prediction[0]), 2)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "Model is loaded and API is healthy"}


st.set_page_config(page_title="Manufacturing Output Predictor")
st.title("📦 Manufacturing Equipment Output Prediction")

# Form for user input
with st.form("prediction_form"):
    st.subheader("Enter Machine Parameters")
    
    Injection_Temperature = st.number_input("Injection Temperature (°C)", min_value=180.0, max_value=250.0)
    Injection_Pressure = st.number_input("Injection Pressure (bar)", min_value=80.0, max_value=150.0)
    Cycle_Time = st.number_input("Cycle Time (s)", min_value=15.0, max_value=45.0)
    Cooling_Time = st.number_input("Cooling Time (s)", min_value=8.0, max_value=20.0)
    Material_Viscosity = st.number_input("Material Viscosity (Pa·s)", min_value=100.0, max_value=400.0)
    Ambient_Temperature = st.number_input("Ambient Temperature (°C)", min_value=18.0, max_value=28.0)
    Machine_Age = st.number_input("Machine Age (years)", min_value=1.0, max_value=15.0)
    Operator_Experience = st.number_input("Operator Experience (months)", min_value=1.0, max_value=120.0)
    Maintenance_Hours = st.number_input("Maintenance Hours Since Last Service", min_value=0.0, max_value=200.0)
    Temperature_Pressure_Ratio = st.number_input("Temperature_Pressure_Ratio", min_value=1.0, max_value=15.0)
    Total_Cycle_Time = st.number_input("Total_Cycle_Time (hours)", min_value=0.0, max_value=120.0)
    Efficiency_Score = st.number_input("Efficiency_Score", min_value=0.0, max_value=200.0)
    Machine_Utilization = st.number_input("Machine_Utilization", min_value=1.0, max_value=200.0)

    submitted = st.form_submit_button("Predict Output")

# API URL
api_url = "http://127.0.0.1:8000/predict"

# Send to FastAPI and display prediction
if submitted:
    input_data = {
        "Injection_Temperature": Injection_Temperature,
        "Injection_Pressure": Injection_Pressure,
        "Cycle_Time": Cycle_Time,
        "Cooling_Time": Cooling_Time,
        "Material_Viscosity": Material_Viscosity,
        "Ambient_Temperature": Ambient_Temperature,
        "Machine_Age": Machine_Age,
        "Operator_Experience": Operator_Experience,
        "Maintenance_Hours": Maintenance_Hours,
        "Temperature_Pressure_Ratio":Temperature_Pressure_Ratio,
        "Total_Cycle_Time":Total_Cycle_Time,
        "Efficiency_Score":Efficiency_Score,
        "Machine_Utilization":Machine_Utilization
        
    }
 
try:
        #response = requests.post(api_url, json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ Predicted Output: {result['Predicted_Output_Parts_Per_Hour']} parts/hour")
        else:
            st.error(f"❌ Error: {response.status_code} - {response.json()['detail']}")
except Exception as e:
        st.error(f"🚨 Could not connect to API: {e}")
