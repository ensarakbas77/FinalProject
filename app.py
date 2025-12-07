from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pickle
import pandas as pd
from pydantic import BaseModel
import warnings

warnings.filterwarnings('ignore')

app = FastAPI()

templates = Jinja2Templates(directory="templates")

try:
    with open("laptop_price_model.pkl", "rb") as f:
        saved_data = pickle.load(f)
        model = saved_data["model"]
        preprocessor = saved_data["preprocessor"]
except Exception as e:
    print(f"Model yükleme hatası: {e}")
    print("Lütfen LaptopPricePredictor.ipynb'u çalıştırarak modeli yeniden eğitin.")
    model = None
    preprocessor = None

class LaptopSpecs(BaseModel):
    brand: str
    processor_brand: str
    processor_name: str
    ram_gb: str
    ssd: str
    hdd: str
    os: str
    weight: str
    Touchscreen: str
    msoffice: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(features: LaptopSpecs):
    if model is None or preprocessor is None:
        return {"error": "Model yüklenemedi. Lütfen modeli yeniden eğitin.", "predicted_price": 0}
    
    try:
        input_data = pd.DataFrame([features.model_dump()])
        processed_data = preprocessor.transform(input_data)
        prediction = model.predict(processed_data)
        return {"predicted_price": float(prediction[0])}
    except Exception as e:
        return {"error": f"Tahmin hatası: {str(e)}", "predicted_price": 0}