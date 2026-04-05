from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models import models
from app.schemas import user_schema
from app.models.database import get_db
from app.middleware.auth_handler import get_password_hash, verify_password, create_access_token
from app.middleware.utils import generate_otp, send_otp_sms, send_welcome_email

router = APIRouter(prefix="/auth", tags=["Authentication"])

# --- Registration API ---
@router.post("/register", response_model=user_schema.UserOut)
def register_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = get_password_hash(user.password)
    
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pwd,
        role=user.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # OTP සහ Email යැවීම
    otp = generate_otp()
    print(f"DEBUG: OTP for {user.username} is {otp}")
    
    # SMS යැවීමට පහළ පේළිය භාවිතා කරන්න (Phone number එකක් තිබේ නම්)
    # send_otp_sms("+94XXXXXXXXX", otp) 
    
    send_welcome_email(user.email, user.username)
    
    return new_user

# --- Login API ---
@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}