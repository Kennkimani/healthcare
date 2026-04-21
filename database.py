##Pushing the data to my database

from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import pandas as pd


load_dotenv()
raw_uri=os.getenv('DATABASE_URL')

df = pd.read_csv("healthcare_dataset.csv")
df['Date of Admission']=pd.to_datetime(df['Date of Admission'])
df['Discharge Date']=pd.to_datetime(df['Discharge Date'])
df['Days_in_hospital']=(df['Discharge Date']-df['Date of Admission']).dt.days
df.drop(['Discharge Date','Date of Admission'],axis=1,inplace=True)

if raw_uri and raw_uri.startswith("postgres://"):
    URI = raw_uri.replace("postgres://", "postgresql://", 1)
else:
    URI = raw_uri


engine = create_engine(URI)
try:
    df.to_sql('patients', con=engine, schema='hospital', if_exists='append', index=False)
finally:
    engine.dispose()  # This explicitly closes the connection


print("Data sent successfully!")