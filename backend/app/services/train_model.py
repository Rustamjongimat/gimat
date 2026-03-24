import os
import joblib
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from app.database import SessionLocal, engine
from app import models

# Avoid printing huge logs
import warnings
warnings.filterwarnings('ignore')

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "ml_models")
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, "hybrid_model.pkl")

def train_hydro_model():
    """Trains a Neural Network (MLP) on historical HydroData from the database."""
    print("Fetching historical data from Database...")
    db = SessionLocal()
    
    # Query all hydro data
    query = db.query(
        models.HydroData.station_id,
        models.HydroData.date,
        models.HydroData.discharge,
        models.HydroData.precipitation,
        models.HydroData.temperature,
        models.HydroData.snow_cover
    ).filter(models.HydroData.discharge != None)
    
    data = []
    for record in query.all():
        data.append({
            "station_id": record.station_id,
            "month": record.date.month,
            "precipitation": record.precipitation or 0,
            "temperature": record.temperature or 0,
            "snow_cover": record.snow_cover or 0,
            "discharge": record.discharge
        })
        
    db.close()
    
    if len(data) < 50:
        raise ValueError(f"Not enough data to train the model. Found only {len(data)} rows.")

    df = pd.DataFrame(data)
    
    print(f"Data Loaded: {len(df)} rows. Preprocessing...")
    
    # Features and Target
    X = df[["station_id", "month", "precipitation", "temperature", "snow_cover"]]
    y = df["discharge"]
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("Training MLP Neural Network...")
    # Multi-layer Perceptron regressor
    mlp = MLPRegressor(
        hidden_layer_sizes=(64, 32, 16),
        activation='relu',
        solver='adam',
        max_iter=500,
        random_state=42,
        early_stopping=True,
        validation_fraction=0.1
    )
    
    mlp.fit(X_train_scaled, y_train)
    
    # Evaluate model
    y_pred = mlp.predict(X_test_scaled)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Model Results -> RMSE: {rmse:.2f}, MAE: {mae:.2f}, R2: {r2:.2f}")
    
    # Save Model and Scaler as a unified dictionary
    model_payload = {
        "model": mlp,
        "scaler": scaler,
        "metrics": {
            "rmse": rmse,
            "mae": mae,
            "r2": r2,
            "nse": r2  # NSE is effectively identical to R2 in this context
        },
        "trained_at": pd.Timestamp.utcnow().isoformat()
    }
    
    joblib.dump(model_payload, MODEL_PATH)
    print(f"Model successfully saved to {MODEL_PATH}")
    return model_payload['metrics']

if __name__ == "__main__":
    train_hydro_model()
