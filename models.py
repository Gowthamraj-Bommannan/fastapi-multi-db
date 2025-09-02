from database import Base
from sqlalchemy import Column, String, Integer

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    mobile_number = Column(String, nullable=False)
    role = Column(String, nullable=False)
    company = Column(String, nullable=False)
