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
    # 1. Email එක දැනටමත් තිබේදැයි පරීක්ෂා කිරීම
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Password එක hash කිරීම
    hashed_pwd = get_password_hash(user.password)
    
    # 3. අලුත් User කෙනෙක් නිර්මාණය කිරීම
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pwd,
        role=user.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # --- Communication (OTP & Email) ---
    
    # 4. OTP එකක් සාදා Console එකේ පෙන්වීම
    otp = generate_otp()
    print(f"DEBUG: OTP for {user.username} is {otp}")
    
    # 5. SMS එකක් යැවීම (ඔයාගේ Twilio Verified number එක මෙතනට දාන්න පුළුවන්)
    # send_otp_sms("+94XXXXXXXXX", otp) 
    
    # 6. Welcome Email එකක් යැවීම (SendGrid හරහා)
    send_welcome_email(user.email, user.username)
    
    return new_user

# --- Login API ---
@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Username එකෙන් User ව සොයා ගැනීම
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    # 2. User නැත්නම් හෝ Password වැරදි නම් Error එකක් දීම
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. සාර්ථක නම් JWT Access Token එකක් සාදා යැවීම
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}