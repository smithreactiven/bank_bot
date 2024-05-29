from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base = declarative_base()


class OwnerReferral(Base):
    __tablename__ = "referral"

    index = Column(Integer, primary_key=True)
    referral_user_id = Column(BigInteger)
    owner_user_id = Column(BigInteger)
