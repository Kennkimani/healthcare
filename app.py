
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd


app = FastAPI(title='HealthCare Model Is Running')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "C:/Users/PC/3D Objects/healthcare project/model.pkl"
# Load model + encoders
model = joblib.load("model.pkl")


#  NO target column here
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
    

@app.get("/")
def home():
    return {'message':'READY TO MAKE PREDICTIONS?'}

@app.post("/reload")
def reload_model():
    """Endpoint for Airflow to trigger a model refresh."""
    global model
    try:
        model = joblib.load(MODEL_PATH)
        return {"status": "Model reloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
def predict(data: PatientData):
    try:
         # Convert input to DataFrame
        input_df = pd.DataFrame([{
            "Name":data.Name,
            "Age": data.Age,
            "Gender": data.Gender,
            "Blood Type": data.Blood_Type,
            "Medical Condition": data.Medical_Condition,
            "Doctor":data.Doctor,
            "Hospital":data.Hospital,
            "Insurance Provider": data.Insurance_Provider,
            "Billing Amount": data.Billing_Amount,
            "Room Number": data.Room_Number,
            "Admission Type": data.Admission_Type,
            "Medication": data.Medication,
            "Days_in_hospital": data.Days_in_hospital
        }])

        # ✅ Predict using pipeline
        prediction = model.predict(input_df)

        return {
            "prediction": prediction.tolist(),
        }
# --- Move these to the very bottom of your app.py ---
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Ensure these lines are NOT inside any other function or dictionary
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse('static/index.html')



           
        }
    except Exception as e:
        return {"error": str(e)}

