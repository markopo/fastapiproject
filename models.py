from sqlalchemy import Column, String, Integer
from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
