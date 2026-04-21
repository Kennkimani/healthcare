import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from sqlalchemy import create_engine
import joblib
import os
from dotenv import load_dotenv

load_dotenv()

# Paths - Use absolute paths to avoid Airflow working directory issues
BASE_DIR = os.getcwd() 
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

DB_URI = os.getenv('DATABASE_URL')

def retrain_from_db(model_file):
    # 1. Fetch data from Postgres
    engine = create_engine(DB_URI)
    try:
        # Pulling data from the 'hospital.patients' table created in database.py
        df = pd.read_sql("SELECT * FROM hospital.patients", con=engine)
    finally:
        engine.dispose()

    if df.empty:
        print("No data found in database. Skipping retraining.")
        return

    # 2. Preprocess (Days_in_hospital is already calculated in your database.py)
    X_new = df.drop(columns=["Test Results"])
    y_new = df["Test Results"]

    # 3. Load, Fit, and Save
    if not os.path.exists(model_file):
        raise FileNotFoundError(f"Original model not found at {model_file}")

    model = joblib.load(model_file)
    model.fit(X_new, y_new)
    joblib.dump(model, model_file)
    
    print(f"Retrained on {len(df)} records. Model updated.")

with DAG(
    dag_id="saturday_model_retrain_v2",
    start_date=datetime(2024, 1, 1),
    schedule="0 12 * * 6",
    catchup=False,
) as dag:

    retrain_task = PythonOperator(
        task_id="fetch_and_retrain",
        python_callable=retrain_from_db,
        op_kwargs={"model_file": MODEL_PATH},
    )
