from fastapi import FastAPI
from app.models import models
from app.models.database import engine
from app.api import auth # මේක අලුතින් එකතු කරන්න

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AuraEnergy AI API")

# Router එක එකතු කිරීම
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "AuraEnergy API is running!"}