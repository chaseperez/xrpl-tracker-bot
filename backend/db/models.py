from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, nullable=False, index=True)
    address = Column(String(128), nullable=False, index=True)
    name = Column(String(64), nullable=True)
    added_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Wallet {self.name or self.address}>"
