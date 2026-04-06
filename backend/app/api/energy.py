from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models import models
from app.schemas import energy_schema
from app.models.database import get_db
from app.middleware.auth_handler import get_current_user # Login වෙලා ඉන්න user ව හඳුනාගන්න

router = APIRouter(prefix="/energy", tags=["Energy Management"])

# 1. විදුලි ඒකක දත්ත පද්ධතියට ඇතුළත් කිරීම (Log Energy Usage)
@router.post("/log", response_model=energy_schema.EnergyOut)
def log_energy(
    data: energy_schema.EnergyCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # අලුත් entry එකක් සෑදීම
    new_entry = models.EnergyUsage(
        kwh_value=data.kwh_value,
        device_id=data.device_id,
        user_id=current_user.id # Login වෙලා ඉන්න user ගේ ID එක auto ගන්නවා
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

# 2. අදාළ User ගේ පැරණි දත්ත ලබා ගැනීම (Get Usage History)
@router.get("/history", response_model=List[energy_schema.EnergyOut])
def get_energy_history(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # Login වෙලා ඉන්න user ට අදාළ දත්ත විතරක් සොයා ගැනීම
    history = db.query(models.EnergyUsage).filter(models.EnergyUsage.user_id == current_user.id).all()
    return history