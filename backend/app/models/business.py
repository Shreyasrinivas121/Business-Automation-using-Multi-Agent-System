from sqlalchemy import Column,Integer,String,TIMESTAMP,text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Business(Base):

    __tablename__ = "businesses"

    business_id = Column(Integer, primary_key=True)

    business_name = Column(String(200))

    email = Column(String(200))

    phone = Column(String(20))

    address = Column(String(500))

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )