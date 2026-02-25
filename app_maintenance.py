from fastapi import FastAPI
import joblib
import pandas as pd
import numpy as np
from pydantic import BaseModel
import uvicorn
import __main__

# 1. Fonction dyal Feature Engineering (khass tkon dejà definie)
def add_features_and_log_transform(X):
    X_new = X.copy()


    if "Torque [Nm]" in X_new.columns and "Rotational speed [rpm]" in X_new.columns:
        X_new["power"] = X_new["Torque [Nm]"] * X_new["Rotational speed [rpm]"]

    if "Process temperature [K]" in X_new.columns and "Air temperature [K]" in X_new.columns:
        X_new["temp_diff"] = X_new["Process temperature [K]"] - X_new["Air temperature [K]"]

    if "Rotational speed [rpm]" in X_new.columns:
        X_new["Rotational speed [rpm]"] = np.log1p(X_new["Rotational speed [rpm]"])

    return X_new


# Trick bach joblib y-l9a l-fonction f l-module l-asli
__main__.add_features_and_log_transform = add_features_and_log_transform

app = FastAPI(title="Maintenance Prediction API")

# 2. Chargement dyal l-Pipeline kamla (Preprocessing + Classifier)
try:
    model = joblib.load("predictive_maintenance_model.pkl")
    print("✅ Pipeline loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")

# Compteur dyal les requêtes
total_scans = 0

@app.get("/system_status")
def system_status():
    global total_scans
    return {
        "model_name": "Random Forest Classifier",
        "total_scans_today": total_scans,
        "status": "🟢 ONLINE"
    }

# 3. Schema dyal l-Input (JSON)
class MachineInput(BaseModel):
    Type: str
    Air_temperature_K: float
    Process_temperature_K: float
    Rotational_speed_rpm: float
    Torque_Nm: float
    Tool_wear_min: float

@app.post("/predict")
def predict(data: MachineInput):
    # 4. DARORI: Retteb l-columns b nefs tartib l-Pipeline (Numeric 3ad Categorical)
    # Had l-tartib hwa li katsennah l-ColumnTransformer dyalk
    input_df = pd.DataFrame([{
        "Air temperature [K]": data.Air_temperature_K,
        "Process temperature [K]": data.Process_temperature_K,
        "Rotational speed [rpm]": data.Rotational_speed_rpm,
        "Torque [Nm]": data.Torque_Nm,
        "Tool wear [min]": data.Tool_wear_min,
        "Type": data.Type  # 'Type' khass ykoun hwa l-lekher b7al f l-Notebook
    }])
    
    # Prediction (l-pipeline ghadi t-transformi o t-predicter)
    prediction = model.predict(input_df)
    
    res = "Failure" if int(prediction[0]) == 1 else "No Failure"
    return {
        "prediction": res,
        "class": int(prediction[0])
    }

@app.post("/predict_proba")
def predict_failure(data: MachineInput):

    input_df = pd.DataFrame([{
        "Air temperature [K]": data.Air_temperature_K,
        "Process temperature [K]": data.Process_temperature_K,
        "Rotational speed [rpm]": data.Rotational_speed_rpm,
        "Torque [Nm]": data.Torque_Nm,
        "Tool wear [min]": data.Tool_wear_min,
        "Type": data.Type  # 'Type' khass ykoun hwa l-lekher b7al f l-Notebook
    }])
    
    # Njebdo la valeur li hdarti 3liha
    valeur_exacte = model.predict_proba(input_df)[0][1]
    
    # Nkharjou resultat
    return {
        "valeur_brut": float(f"{valeur_exacte*100:.2f}"),
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)