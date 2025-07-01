from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True)
    chat_id = Column(String, index=True)
    address = Column(String, index=True)
    added_at = Column(DateTime, default=datetime.utcnow)