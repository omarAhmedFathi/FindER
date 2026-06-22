import uuid
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base
from sqlalchemy.sql import func
import enum


class ResourceType(str, enum.Enum):
    AMBULANCE = "AMBULANCE"
    FIRE_TRUCK = "FIRE_TRUCK"
    HELO = "HELO"
    SUPPLY_DROP = "SUPPLY_DROP"


class Resource(Base):
    __tablename__ = "resources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=True)
    type = Column(SAEnum(ResourceType, native_enum=False), nullable=False)
    status = Column(String(50), default="AVAILABLE")
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("emergencies.id"), nullable=True)
    location_lat = Column(Numeric(10, 8), nullable=False)
    location_lon = Column(Numeric(11, 8), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
