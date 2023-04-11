import requests

payload = {
    "model_key": "Citroën",
    "mileage": 150411,
    "engine_power": 100,
    "fuel": "diesel",
    "paint_color": "green",
    "car_type": "convertible",
    "private_parking_available": True,
    "has_gps": True,
    "has_air_conditioning": True,
    "automatic_car": True,
    "has_getaround_connect": True,
    "has_speed_regulator": True,
    "winter_tires": True
}

r = requests.post("http://localhost:4000/predict", json=payload)
print(r.json())
