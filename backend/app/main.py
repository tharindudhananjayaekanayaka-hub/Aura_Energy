from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # අලුතින් එකතු කළා
from app.models import models
from app.models.database import engine
from app.api import auth, energy

# Database එකේ tables නොමැති නම් ඒවා නිර්මාණය කිරීම
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AuraEnergy AI API")

# --- CORS Setup (Frontend එක connect කිරීමට ඉතා වැදගත්) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # React frontend එක දුවන URL එක (http://localhost:3000) සඳහා අවසර දේ
    allow_credentials=True,
    allow_methods=["*"], # GET, POST, PUT, DELETE ඔක්කොටම ඉඩ දේ
    allow_headers=["*"],
)

# Routers එකතු කිරීම
app.include_router(auth.router)
app.include_router(energy.router)

@app.get("/")
def read_root():
    return {
        "message": "AuraEnergy API is running successfully!",
        "status": "Online",
        "version": "1.0.0"
    }