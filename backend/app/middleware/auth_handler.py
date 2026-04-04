from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

load_dotenv()

# Password hash කරන්න පාවිච්චි කරන එක
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# .env එකෙන් දත්ත ලබා ගැනීම
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Password එක Hash කරන්න
def get_password_hash(password):
    return pwd_context.hash(password)

# එවන password එක සහ hash එක ගැලපෙනවාද බලන්න
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# JWT Token එකක් නිර්මාණය කරන්න
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt