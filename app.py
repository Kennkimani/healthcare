from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import joblib
import pandas as pd
import os

app = FastAPI(title='HealthCare Model Is Running')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use relative path for the cloud
MODEL_PATH = "model.pkl"
model = joblib.load(MODEL_PATH)

class PatientData(BaseModel):
    Name: str
    Age: float = Field(ge=0, le=120)
    Gender: str
    Blood_Type: str
    Medical_Condition: str
    Doctor: str
    Hospital: str
    Insurance_Provider: str
    Billing_Amount: float
    Room_Number: int
    Admission_Type: str
    Medication: str
    Days_in_hospital: int

@app.post("/reload")
def reload_model():
    global model
    try:
        model = joblib.load(MODEL_PATH)
        return {"status": "Model reloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
def predict(data: PatientData):
    try:
        input_df = pd.DataFrame([{
            "Name": data.Name,
            "Age": data.Age,
            "Gender": data.Gender,
            "Blood Type": data.Blood_Type,
            "Medical Condition": data.Medical_Condition,
            "Doctor": data.Doctor,
            "Hospital": data.Hospital,
            "Insurance Provider": data.Insurance_Provider,
            "Billing Amount": data.Billing_Amount,
            "Room Number": data.Room_Number,
            "Admission Type": data.Admission_Type,
            "Medication": data.Medication,
            "Days_in_hospital": data.Days_in_hospital
        }])

        prediction = model.predict(input_df)
        return {"prediction": prediction.tolist()}
    except Exception as e:
        return {"error": str(e)}

# Static files and Frontend route
# Make sure you have a folder named 'static' with your html, css, and js files!
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse('static/index.html')


