from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
import joblib
import pandas as pd

df=pd.read_csv('healthcare_dataset.csv')
df['Date of Admission']=pd.to_datetime(df['Date of Admission'])
df['Discharge Date']=pd.to_datetime(df['Discharge Date'])
df['Days_in_hospital']=(df['Discharge Date']-df['Date of Admission']).dt.days
df.drop(['Discharge Date','Date of Admission'],axis=1, inplace=True, errors='ignore')

X = df.drop(columns="Test Results")
y = df["Test Results"]

categorical_cols = X.select_dtypes(include="object").columns
numeric_cols = X.select_dtypes(include="number").columns

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", "passthrough", numeric_cols)
    ]
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", DecisionTreeClassifier())
])

pipeline.fit(X, y)

joblib.dump(pipeline, "model.pkl")