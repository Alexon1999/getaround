import mlflow
import uvicorn
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI
import joblib
import warnings

warnings.filterwarnings('ignore')

description = """
Welcome to Getaround's API 😃

## Introduction Endpoints

Here are two endpoints you can try:
* `/`: **GET** request that display a simple default message.
* `/predict`: **POST** request to get predictions.


## Car Rental Price Prediction

This is an endpoint that uses a State-of-the-art **Machine Learning** model to help you determine the optimum car rental price based on the characteristics of the car.

* `/predict` that accepts `json`


Check out documentation below 👇 for more information on each endpoint. 
"""

tags_metadata = [
    {
        "name": "Introduction Endpoints",
        "description": "Simple endpoints to try out!",
    },

    {
        "name": "Car Rental Price Prediction",
        "description": "Get a suggestion of car rental price per day based on the characteristics of the car"
    }
]

app = FastAPI(
    title="Getaround API",
    description=description,
    version="0.1",
    contact={
        "name": "Getaround"
    },
    openapi_tags=tags_metadata
)


class PredictionFeatures(BaseModel):
    model_key: str = "Citroën"
    mileage: int = 150000
    engine_power: int = 100
    fuel: str = "diesel"
    paint_color: str = "green"
    car_type: str = "convertible"
    private_parking_available: bool = True
    has_gps: bool = True
    has_air_conditioning: bool = True
    automatic_car: bool = True
    has_getaround_connect: bool = True
    has_speed_regulator: bool = True
    winter_tires: bool = True


@app.get("/", tags=["Introduction Endpoints"])
async def index():
    """
    Simply returns a welcome message!
    """
    message = "Hello world! This `/` is the most simple and default endpoint. If you want to learn more, check out documentation of the api at `/docs`"
    return {
        'message': message
    }


@app.post("/predict", tags=["Car Rental Price Prediction"])
async def predict(prediction_features: PredictionFeatures):
    """
    Prediction of Optimimum Rental Price
    """
    # Read data
    car_to_rent = pd.DataFrame(
        {
            "model_key": [prediction_features.model_key],
            "mileage": [prediction_features.mileage],
            "engine_power": [prediction_features.engine_power],
            "fuel": [prediction_features.fuel],
            "paint_color": [prediction_features.paint_color],
            "car_type": [prediction_features.car_type],
            "private_parking_available": [prediction_features.private_parking_available],
            "has_gps": [prediction_features.has_gps],
            "has_air_conditioning": [prediction_features.has_air_conditioning],
            "automatic_car": [prediction_features.automatic_car],
            "has_getaround_connect": [prediction_features.has_getaround_connect],
            "has_speed_regulator": [prediction_features.has_speed_regulator],
            "winter_tires": [prediction_features.winter_tires],
        }
    )

    # Log model from mlflow
    logged_model = 'runs:/65a4c9bc02894e91ae2f325645514393/getaround-optimum-prices'

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    # If you want to load model persisted locally
    # loaded_model = joblib.load('data/RandomForestRegressor.joblib')

    prediction = loaded_model.predict(car_to_rent)

    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)
