from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.database.db import Base

class Report(Base):

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    reporter_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    reported_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    report_description = Column(String(500), nullable=False)

    status = Column(String(20), default="Pending")

    created_at = Column(DateTime, server_default=func.now())

    resolved_at = Column(DateTime)

    reporter = relationship("User", foreign_keys=[reporter_id])
    reported_user = relationship("User", foreign_keys=[reported_user_id])

