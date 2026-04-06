from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
    
    # User ට අදාළ energy data සම්බන්ධ කිරීම
    usage_entries = relationship("EnergyUsage", back_populates="owner")

class EnergyUsage(Base):
    __tablename__ = "energy_usage"
    id = Column(Integer, primary_key=True, index=True)
    kwh_value = Column(Float, nullable=False) # විදුලි ඒකක ප්‍රමාණය
    timestamp = Column(DateTime, default=datetime.utcnow) # දත්ත ලැබුණු වෙලාව
    device_id = Column(String, nullable=True) # උපාංගයේ අංකය (ඇත්නම්)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="usage_entries")