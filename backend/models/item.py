from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from backend.database.db import Base

class Item(Base): 

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)

    report = Column(String(100), nullable=False)

    title = Column(String(100), nullable=False)

    description = Column(Text)

    category = Column(Integer, ForeignKey("categories.id"), nullable=False)

    status = Column(String(50), default="Active")

    location = Column(String(500), nullable=False)

    image_url = Column(String(255), nullable=False)

    reported_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, server_default=func.now())

