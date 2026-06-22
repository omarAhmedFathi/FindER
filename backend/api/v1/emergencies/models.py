import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Numeric, Enum as SAEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base
from sqlalchemy.sql import func
import enum


class EmergencyStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ROUTED = "ROUTED"
    RESOLVED = "RESOLVED"
    FALSE_ALARM = "FALSE_ALARM"


class Emergency(Base):
    __tablename__ = "emergencies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    status = Column(SAEnum(EmergencyStatus, native_enum=False), default=EmergencyStatus.ACTIVE)
    location_lat = Column(Numeric(10, 8), nullable=False)
    location_lon = Column(Numeric(11, 8), nullable=False)
    description = Column(String, nullable=True)
    severity = Column(Integer, default=3)
    detected_via_nlp = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
