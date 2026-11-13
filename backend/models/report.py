from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.database.db import Base

class Report(Base):

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    reported_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    report_description = Column(String(500), nullable=False)

    status = Column(String(20), default="pending")

    created_at = Column(DateTime, server_default=func.now())

    admin_note = Column(String(500))

    resolved_at = Column(DateTime)

