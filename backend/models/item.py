from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from database.db import Base

class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False)

    description = Column(Text)

    category = Column(Integer, ForeignKey("categories.id"), nullable=False)

    status = Column(String(50), default="Active")

    location = Column(String(255))

    image_url = Column(String(255), nullable=False)

    reported_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, server_default=func.now())

