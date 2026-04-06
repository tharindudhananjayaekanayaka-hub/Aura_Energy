from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# දත්ත ඇතුළත් කරන විට අවශ්‍ය දේවල්
class EnergyCreate(BaseModel):
    kwh_value: float
    device_id: Optional[str] = None

# දත්ත ආපසු පෙන්වන විට ලැබෙන දේවල්
class EnergyOut(BaseModel):
    id: int
    kwh_value: float
    timestamp: datetime
    user_id: int

    class Config:
        from_attributes = True