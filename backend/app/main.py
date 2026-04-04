from fastapi import FastAPI
from app.models import models
from app.models.database import engine

# මේ පේළියෙන් තමයි Supabase එකේ tables (users, energy_logs) ඔටෝමැටිකව හැදෙන්නේ
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AuraEnergy AI API")

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "message": "Welcome to AuraEnergy AI Backend!",
        "database": "Connected to Supabase"
    }