from src.database import Base
from datetime import datetime
from sqlalchemy import Integer, Column, String, TIMESTAMP, Date


class Registration(Base):
    __tablename__ = "auth_test_fastapi"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(25), nullable=False, unique=True)
    hashed_password = Column(String(256), nullable=False)