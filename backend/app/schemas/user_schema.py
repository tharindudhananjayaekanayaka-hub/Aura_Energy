from pydantic import BaseModel, EmailStr
from typing import Optional

# User කෙනෙක් register වෙද්දී එවන දත්ත
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "technician"

# User කෙනෙක්ව ආපසු පෙන්වද්දී දෙන දත්ත (Password එක මේකේ නැහැ!)
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

# Login වෙද්දී අවශ්‍ය දත්ත
class UserLogin(BaseModel):
    username: str
    password: str

# Token එකක් ලබා දෙන ආකාරය
class Token(BaseModel):
    access_token: str
    token_type: str